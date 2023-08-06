# Copyright 2017, OpenCensus Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import aiohttp

from opencensus.trace.tracers.noop_tracer import NoopTracer
from qubit.opencensus.trace import asyncio_context

log = logging.getLogger(__name__)

MODULE_NAME = 'aiohttp'


def trace_integration(tracer=None, propagator=None):
    """Wrap the requests library to trace it."""
    log.info('Integrated module: {}'.format(MODULE_NAME))
    # Wrap the aiohttp functions
    aiohttp_func = getattr(aiohttp.ClientSession, '_request')
    wrapped = wrap_aiohttp(aiohttp_func, propagator=propagator)
    setattr(aiohttp.ClientSession, aiohttp_func.__name__, wrapped)


def wrap_aiohttp(aiohttp_func, propagator=None):
    """Wrap the aiohttp function to trace it."""
    async def call(*args, **kwargs):
            _tracer = asyncio_context.get_opencensus_tracer()
            if _tracer is None or isinstance(_tracer, NoopTracer):
                return await aiohttp_func(*args, **kwargs)

            parent_span = _tracer.current_span()
            _span = parent_span.span(name='[aiohttp] {}'.format(args[1]))
            _span.add_attribute('aiohttp/method', str(args[1]))
            _span.add_attribute('aiohttp/url', str(args[2]))

            span_context =  _tracer.span_context
            if propagator is not None:
                headers = propagator.to_headers(span_context)
                if 'headers' not in kwargs:
                    kwargs['headers'] = {}
                for k, v in headers.items():
                    kwargs['headers'][k] = v

            try:
                _span.start()
                response = await aiohttp_func(*args, **kwargs)

                _span.add_attribute(
                    'aiohttp/status_code', str(response.status))
                _span.add_attribute(
                    'aiohttp/status_reason', str(response.reason))

                if response.status >= 500:
                    _span.add_attribute(
                        'error', True)

                return response
            except Exception as e:
                _span.add_attribute(
                    'error', True)
                _span.add_attribute(
                    'error.message', str(e))
                raise e
            finally:
                _span.finish()

    return call
