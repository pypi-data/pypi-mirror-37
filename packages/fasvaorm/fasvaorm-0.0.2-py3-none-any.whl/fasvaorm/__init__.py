# -*- tab-width: 4; encoding: utf-8; -*-
# ex: set tabstop=4 expandtab:
# Copyright (c) 2016-2018 by Lars Klitzke, Lars.Klitzke@hs-emden-leer.de.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine as SQLAlchemyEngine

# A global database factory
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as SQLALchemySession

from fasvaorm.models import *

SessionFactory = None

# The global database session
DBSession = None

# The global database SQLAlchemy engine
Engine = None


class EngineNotInitializedError(RuntimeError):
    pass


def cleanup():
    """
    Remove all references.
    """
    global DBSession, SessionFactory, Engine

    DBSession = None
    SessionFactory = None
    Engine = None


def get_session(new=False):
    """
    Get the current active session or create a new one

    Returns:
        SQLALchemySession: The current active global session

    """

    if new:
        factory = get_session_factory()

        return factory()
    else:
        global DBSession

        # check if the global session is initialized
        if not DBSession:
            # if this is not the case, setup a session
            DBSession = init_session()

        return DBSession


def get_session_factory():
    """
    Get the current active session factory

    Returns:
        sessionmaker: The session factory
    """

    global SessionFactory

    # verify that the session is initialized
    if not SessionFactory:
        # otherwise setup the session factory
        SessionFactory = init_session_factory()

    return SessionFactory


def get_engine():
    """
    Get the current active engine

    Returns:
        Engine: The current engine
    """
    global Engine
    return Engine


def set_engine(engine):
    """
    Set the current active engine

    Args:
        engine (SQLAlchemyEngine): The new global engine
    """

    global Engine
    Engine = engine


def init_engine(url, **kwargs):
    """
    Initialize the global SQLAlchemy database engine

    Args:
        url (str):  URL to connect with
        **kwargs:   Arguments passed to the `create_engine()` function.

    Returns:
        SQLAlchemyEngine: The global engine
    """
    engine = get_engine()

    # only init the global engine once
    if not engine:
        engine = create_engine(url, **kwargs)

    set_engine(engine)

    return engine


def init_session_factory(engine=None):
    """
    Initialize the global database session factory

    Args:
        engine (SQLAlchemyEngine): The SQLALchemy engine

    Returns:
        sessionmaker: The session factory to create sessions with

    Raises:
        EngineNotInitializedError: If the passed engine (if defined) or the global engine is not initialized.
    """

    if not engine:
        engine = get_engine()

    if not engine:
        raise EngineNotInitializedError('Either pass a engine to use or initialize the global engine.')

    global SessionFactory

    # only init the global session factory once
    if not SessionFactory:
        SessionFactory = sessionmaker(bind=engine)

    return SessionFactory


def init_session(factory=None):
    """
    Initialize the global SQLAlchemy database session

    Args:
        factory (sessionmaker): The session maker to create the session with

    Returns:
        SQLALchemySession: The global database session
    """
    if not factory:
        factory = get_session_factory()

    global DBSession
    # only init the global session once
    if not DBSession:
        DBSession = factory()

    return DBSession


def close_session(session=None):
    """
    Closes either the given or the global session.

    Args:
        session (SQLAlchemySession): The sesssion to close
    """
    if not session:
        session = get_session()

    session.flush()
    session.close()
