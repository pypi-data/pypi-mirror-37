# -*- coding: utf8 -*-
import types
import copy
from .base_callback import BaseCallback

_TF_PATCHED_RUN = {}


class TfSessionRunPatchContext(object):
    def __init__(self, patcher_method, monitored_fetches, session_instance):
        self._patcher_method = patcher_method
        self._monitored_fetches = monitored_fetches
        self._session_instance = session_instance

    @classmethod
    def _generate_unique_key(cls, existing_keys):
        while True:
            key = BaseCallback.generate_tag()
            if key not in existing_keys:
                return key

    @classmethod
    def run_session(cls, monitored_fetches, session, fetches, feed_dict=None, options=None, run_metadata=None):
        all_fetches = copy.copy(monitored_fetches)

        key_for_unmonitored_fetches = cls._generate_unique_key(all_fetches.keys())
        all_fetches[key_for_unmonitored_fetches] = fetches

        monitored_results = cls._run_session(session, all_fetches, feed_dict, options, run_metadata)

        unmonitored_results = monitored_results.pop(key_for_unmonitored_fetches, {})

        return monitored_results, unmonitored_results

    @classmethod
    def _run_session(cls, session, fetches, feed_dict=None, options=None, run_metadata=None):
        patched_method = _TF_PATCHED_RUN.get(session)
        if patched_method is not None:
            return patched_method(fetches, feed_dict, options, run_metadata)

        patched_method = _TF_PATCHED_RUN.get(type(session))
        if patched_method is not None:
            return patched_method(session, fetches, feed_dict, options, run_metadata)

        raise KeyError('Session not patched')

    @classmethod
    def _patch_run_classes(cls, patched_run):
        import tensorflow as tf

        for klass in (tf.Session, tf.InteractiveSession):
            _TF_PATCHED_RUN[klass] = klass.run
            klass.run = patched_run

    @classmethod
    def _patch_run_instance(cls, patched_run, session_instance):
        if session_instance in _TF_PATCHED_RUN:
            return

        _TF_PATCHED_RUN[session_instance] = session_instance.run
        session_instance.run = types.MethodType(patched_run, session_instance)

    def _unpatch_run(self, klasses):
        for klass in klasses:
            if klass not in _TF_PATCHED_RUN:
                continue

            klass.run = _TF_PATCHED_RUN[klass]
            del _TF_PATCHED_RUN[klass]

        if self._session_instance is not None:
            self._session_instance.run = _TF_PATCHED_RUN[self._session_instance]

    def __enter__(self):
        patched_run = self._patcher_method(self._monitored_fetches)

        if self._session_instance is None:
            self._patch_run_classes(patched_run)
        else:
            self._patch_run_instance(patched_run, self._session_instance)

        return self

    def __exit__(self, *exc):
        self._reset_tf_session()

    def _reset_tf_session(self):
        import tensorflow as tf

        if self._session_instance is None:
            self._unpatch_run((tf.Session, tf.InteractiveSession))
        else:
            self._unpatch_run(())
