import functools

from coincurve import PrivateKey
from flask import (Blueprint, Response, g, redirect, render_template, request,
                   session, url_for)
from flask_babel import Babel
from sqlalchemy import func

from .broadcast import broadcast_move
from .move import LevelUp, Move
from .node import Node
from .orm import db
from .user import User, cache


game = Blueprint('game', __name__, template_folder='templates')
babel = Babel()


@babel.localeselector
def get_locale():
    langs = {babel.default_locale}
    langs.update(babel.list_translations())
    return request.accept_languages.best_match([l.language for l in langs])


def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        private_key_hex = session.get('private_key')
        error = None
        if private_key_hex is not None:
            if private_key_hex.startswith(('0x', '0X')):
                private_key_hex = private_key_hex[2:]
            try:
                private_key_bytes = bytes.fromhex(private_key_hex)
                private_key = PrivateKey(private_key_bytes)
            except (ValueError, TypeError):
                error = 'invalid-private-key'
            else:
                g.user = User(private_key)
                return f(*args, **kwargs)
        return redirect(url_for('.get_login', next=request.url, error=error))
    return decorated_function


@game.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')


@game.route('/login', methods=['POST'])
def post_login():
    session['name'] = request.values.get('name')
    session['private_key'] = request.values.get('private_key')
    if 'next' in request.values:
        return redirect(request.values.get('next'))
    else:
        return redirect(url_for('.get_game'))


@game.route('/logout', methods=['GET'])
@login_required
def get_logout():
    del session['private_key']
    return redirect(url_for('game.get_login'))


@cache.memoize(60)
def get_rank():
    return db.session.query(
        LevelUp.user_address, func.count(LevelUp.id)
    ).group_by(LevelUp.user_address).order_by(
        func.count(LevelUp.id).desc()
    ).limit(10).all()


def get_unconfirmed_move(address):
    unconfirmed_moves = Move.query.filter_by(
        user_address=address, block=None
    )
    for unconfirmed_move in unconfirmed_moves:
        if unconfirmed_move.valid:
            return unconfirmed_move
    return None


@game.route('/dashboard')
@login_required
def get_dashboard():
    if not g.user.avatar():
        return redirect(url_for('.get_new_novice'))

    unconfirmed_move = get_unconfirmed_move(g.user.address)

    feed = g.user.moves
    # for caching
    for move in reversed(feed.limit(10).all()):
        avatar, result = move.execute()
    return render_template('dashboard.html',
                           unconfirmed_move=unconfirmed_move,
                           feed=feed.order_by(Move.block_id.desc()),
                           rank=get_rank())


@game.route('/')
@login_required
def get_game():
    avatar = g.user.avatar()
    if not avatar:
        return redirect(url_for('.get_new_novice'))
    if avatar.class_ == 'novice':
        return redirect(url_for('.get_first_class'))

    return render_template('game.html')


@game.route('/status')
@login_required
def get_status():
    if not g.user.avatar():
        return redirect(url_for('.get_new_novice'))

    feed = g.user.moves
    # for caching
    for move in reversed(feed.limit(10).all()):
        avatar, result = move.execute()
    return render_template('status.html',
                           feed=feed.order_by(Move.block_id.desc()))


@game.route('/in_progress')
@login_required
def get_unconfirmed():
    if not g.user.avatar():
        return redirect(url_for('.get_new_novice'))

    unconfirmed_move = get_unconfirmed_move(g.user.address)
    if unconfirmed_move:
        return "true"
    return "false"


@game.route('/new')
@login_required
def get_new_novice():
    if not g.user.avatar():
        move = Move.query.filter_by(
            user_address=g.user.address,
            name='create_novice',
        ).first()
        if not move:
            move = g.user.create_novice({'name': session.get('name', '')})
            db.session.add(move)
            db.session.commit()
            serialized = move.serialize(
                use_bencode=False,
                include_signature=True,
                include_id=True,
            )
            broadcast_move(
                serialized,
                my_node=Node(url=f'{request.scheme}://{request.host}')
            )
        return render_template('new.html', move=move)
    return redirect(url_for('.get_game'))


@game.route('/first_class')
@login_required
def get_first_class():
    avatar = g.user.avatar()
    if not avatar:
        return redirect(url_for('.get_new_novice'))
    if avatar.class_ != 'novice':
        return redirect(url_for('.get_game'))

    return render_template('first_class.html')


@game.route('/session_moves', methods=['POST'])
@login_required
def post_move():
    unconfirmed_move = get_unconfirmed_move(g.user.address)

    if unconfirmed_move:
        return redirect(url_for('.get_game'))

    if request.values.get('name') == 'hack_and_slash':
        if g.user.avatar().dead:
            return redirect(url_for('.get_game'))
        move = g.user.hack_and_slash(request.values.get('weapon'),
                                     request.values.get('armor'),
                                     request.values.get('food'),)
    if request.values.get('name') == 'sleep':
        move = g.user.sleep()
    if request.values.get('name') == 'level_up':
        move = g.user.level_up(request.values.get('new_status'))
    if request.values.get('name') == 'say':
        move = g.user.say(request.values.get('content'))
    if request.values.get('name') == 'send':
        move = g.user.send(request.values.get('item'),
                           request.values.get('amount'),
                           request.values.get('receiver'))
    if request.values.get('name') == 'combine':
        move = g.user.combine(request.values.get('item1'),
                              request.values.get('item2'),
                              request.values.get('item3'))
    if request.values.get('name') == 'first_class':
        move = g.user.first_class(request.values.get('class_'))
    if request.values.get('name') == 'move_zone':
        move = g.user.move_zone(request.values.get('zone'))

    if move:
        serialized = move.serialize(
            use_bencode=False,
            include_signature=True,
            include_id=True,
        )
        broadcast_move(
            serialized,
            my_node=Node(url=f'{request.scheme}://{request.host}')
        )
    return redirect(url_for('.get_game'))


@game.route('/export/', methods=['GET'])
@login_required
def export_private_key():
    key = session['private_key']
    file_name = f'{g.user.address}.csv'
    return Response(
        key,
        headers={
            'Content-Disposition': f'attachment;filename={file_name}',
            'Content-Type': 'text/csv',
        }
    )
