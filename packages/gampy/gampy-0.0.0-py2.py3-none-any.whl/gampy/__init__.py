# from typing import Callable, Iterable


# class Error(Exception):
#     """Base class for errors."""

#     pass


# class DefinitionError(Error):
#     """Error during program definition."""

#     pass


# class ExecutionError(Error):
#     """Error during program execution."""

#     pass


# class Program(object):
#     """Program as a sequence of steps."""

#     def __init__(self, *steps):
#         """Initialize the program steps."""
#         self.steps = steps  # trigger setter

#     # PROPERTY

#     @property
#     def steps(self):
#         """Return the program steps."""
#         return self._steps

#     @steps.setter
#     def steps(self, steps):
#         """Append steps to the program."""
#         self._steps = []

#         for s in steps:
#             # fill blanks
#             if len(s) == 1:
#                 step = (s[0], list(), dict())
#             elif len(s) == 2:
#                 step = (s[0], s[1], dict())
#             elif len(s) == 3:
#                 step = (s[0], s[1], s[2])
#             else:
#                 raise DefinitionError(
#                     f"The number of step arguments should be between 1 and 3. Got: {len(steps)}"
#                 )

#             # validate steps
#             if not isinstance(step[0], Callable):
#                 raise DefinitionError(
#                     f"The first step argument should be Callable. Got: {type(step[0]).__name__}"
#                 )
#             elif not isinstance(step[1], Iterable):
#                 raise DefinitionError(
#                     f"The second step argument should be Iterable. Got: {type(step[1]).__name__}"
#                 )
#             elif not isinstance(step[2], Iterable):
#                 raise DefinitionError(
#                     f"The third step argument should be Iterable. Got: {type(step[2]).__name__}"
#                 )

#             self._steps.append(step)

#     # FORMAT

#     def __str__(self):
#         """Return a string from the program steps."""

#         def fmt(step):
#             f, args, kwargs = step

#             strf = f.__name__
#             strargs = [str(x) for x in args]
#             strkwargs = [f"{k}={v}" for k, v in kwargs.items()]

#             return f"{strf}({', '.join(strargs + strkwargs) })"

#         return "\n".join(map(fmt, self.steps))

#     def __repr__(self):
#         """Return a representation of the program steps."""
#         return str(self.steps)

#     # ALGEBRA

#     def __add__(self, other):
#         """Combine program steps."""
#         return self.__class__(self.steps + other.steps)

#     def __sub__(self, other):
#         """Filter program steps."""
#         steps = []

#         for s in self.steps:
#             if s not in other:
#                 steps.append(s)

#         return self.__class__(steps)

#     def __mul__(self, n):
#         """Duplicate program steps."""
#         return self.__class__(self._steps * 2)

#     def __matmul__(self, g):
#         """Compose program functions."""
#         return self.__class__((g(f), args, kwargs) for f, args, kwargs in self.steps)

#     def __truediv__(self, n):
#         """Chunk steps in smaller programs."""
#         chunk = []

#         for i, s in enumerate(self.steps, 1):
#             chunk.append(s)

#             if i % n == 0:
#                 yield self.__class__(*chunk)
#                 chunk.clear()

#     def __floordiv__(self, n):
#         """Chunk all steps in smaller programs."""
#         chunk = []

#         for i, x in enumerate(self.steps, 1):
#             chunk.append(x)

#             if i % n == 0:
#                 yield self.__class__(*chunk)
#                 chunk.clear()

#         if chunk:
#             yield self.__class__(*chunk)

#     def __mod__(self, other):
#         """Alternate program steps."""
#         gen = it.chain.from_iterable(it.zip_longest(self.steps, other.steps))

#         steps = [s for s in gen if s is not None]

#         return self.__class__(steps)

#     def __pow__(self, other):
#         pass

#     def __lshift__(self, n):
#         """Shift program steps to the left."""
#         return self.__class__(self.steps[n:] + self.steps[:n])

#     def __rshift__(self, n):
#         """Shift program steps to the right."""
#         return self.__class__(self.steps[-n:] + self.steps[:-n])

#     def __and__(self, other):
#         """Intersect program steps."""
#         steps = []

#         for s in self.steps:
#             if s in other:
#                 steps.append(s)

#         return self.__class__(steps)

#     def __xor__(self, other):
#         """Symmetric program steps."""
#         return (self + other) - (self & other)

#     def __or__(self, other):
#         pass

#     # INPLACE

#     def __iadd__(self, other):
#         """Combine program steps."""
#         self._steps += other.steps

#     def __isub__(self, other):
#         """Filter program steps."""
#         steps = []

#         for s in self.steps:
#             if s not in other:
#                 steps.append(s)

#         self._steps = steps

#     def __imul__(self, n):
#         """Duplicate program steps"""
#         self._steps = self.steps * n

#     def __imatmul__(self, g):
#         """Combine program functions."""
#         self._steps = [(g(f), args, kwargs) for f, args, kwargs in self.steps]

#     def __imod__(self, other):
#         """Alternate program steps."""
#         gen = it.chain.from_iterable(it.zip_longest(self.steps, other.steps))

#         self._steps = [s for s in gen if s is not None]

#     def __ipow__(self, other):
#         pass

#     def __ilshift__(self, n):
#         """Shift program steps to the left."""
#         self._steps = self.steps[n:] + self.steps[:n]

#     def __irshift__(self, n):
#         """Shift program steps to the right."""
#         self.steps = self.steps[-n:] + self.steps[:-n]

#     def __iand__(self, other):
#         """Intersect program steps."""
#         steps = []

#         for s in self.steps:
#             if s in other:
#                 steps.append(s)

#         self._steps = steps

#     def __ixor__(self, other):
#         """Symmetric program steps."""
#         self._steps = (self ^ other).steps

#     def __ior__(self, other):
#         pass

#     # CONTEXT

#     def __enter__(self):
#         """Return the program steps."""
#         return self.steps

#     def __exit__(self, exc_type, exc_value, traceback):
#         """Update the program steps."""
#         self.steps = self._steps  # trigger setter

#     # CALLABLE
#     def __call__(self, state, control=None):
#         """Execute program steps."""
#         try:
#             for step in self.steps:
#                 if control is not None:
#                     step, state = control(step, state)

#                 f, args, kwargs = step
#                 state = f(*args, **kwargs)

#             return state
#         except Exception as err:
#             raise ExecutionError() from err

#     # CONVERTER

#     def __bool__(self):
#         """Return True if program is not empty."""
#         return len(self.steps) > 0

#     # COLLECTION

#     def __len__(self):
#         """Return the number of steps."""
#         return len(self.steps)

#     def __iter__(self):
#         """Iterate over the program steps."""
#         return iter(self.steps)

#     def __reversed__(self):
#         """Reverse the steps of the program."""
#         return self.__init__(*reversed(self.steps))

#     def __getitem__(self, n):
#         """Return the n step of the program."""
#         return self.steps[n]

#     def __delitem__(self, n):
#         """Delete the n step of the program."""
#         del self.steps[n]

#     def __setitem__(self, n, step):
#         """Change the n step of the program."""
#         self.steps[n] = step

#     def __contains__(self, step):
#         """Return True if step exists in the program."""
#         return step in self.steps

#     # COMPARABLE

#     def __lt__(self, other):
#         """Compare the program lengths with <."""
#         return len(self) < len(other)

#     def __le__(self, other):
#         """Compare the program lengths with <=."""
#         return len(self) <= len(other)

#     def __eq__(self, other):
#         """Compare the program lengths with ==."""
#         return len(self) == len(other)

#     def __ne__(self, other):
#         """Compare the program lengths with !=."""
#         return len(self) != len(other)

#     def __ge__(self, other):
#         """Compare the program lengths with >=."""
#         return len(self) >= len(other)

#     def __gt__(self, other):
#         """Compare the program lengths with >."""
#         return len(self) > len(other)


# # promise to store state
# # append f as args


# # def optional(default):
# #     def decorator(f):
# #         @wraps(f)
# #         def decorated(*args, **kwargs):
# #             state = f(*args, **kwargs)

# #             if state is None:
# #                 return default

# #         return decorated

# #     return decorator


# # def Except(on=Exception):
# #     def except_(f, args, kwargs, state):
# #         if issubclass(state, on):
# #             return state

# #         try:
# #             state = f(*args, **kwargs)
# #         except on as ex:
# #             return ex

# #     return except_

# # class Pipe(Program):
# #     FIRST = 0
# #     LAST = -1

# #     def __init__(self, *steps, n=FIRST):
# #         super().__init__(*steps, {"n": n})

# #     def __call__(self, state=None):
# #         """Call the program and inject state"""
# #         for f, args, kwargs in self.steps:
# #             args_ = args.copy()

# #             if self.n < 0:
# #                 args_.append(state)
# #             else:
# #                 args_.insert(self.n, state)

# #             return f(*args_, **kwargs)


# # class Block(Program):
# #     def __call__(self, state=None):
# #         """Call the program and ignore state"""
# #         for f, args, kwargs in self.steps:
# #             return f(*args, **kwargs)


# # def Context():
# #     pass


# # def Capture():
# #     # capture stdout/stderr
# #     pass


# # def Memoize():
# #     pass


# # def Log():
# #     pass


# # def Pre(do):
# #     def pre(f, args, kwargs, state):
# #         pre(f, args, kwargs, state)

# #         return f(args, kwargs, state)

# #     return pre


# # def Post(do):
# #     def post(f, args, kwargs, state):
# #         state = f(args, kwargs, state)
# #         do(f, args, kwargs, state)

# #         return state

# #     return post


# # # Cache: cache f/args

# # # Cat: (list monad)

# # # Lazy: convert to gen

# # # Watch: pre/post fn

# # # Strict: convert to list

# # # Ident: imperative style

# # # Do: independent actions

# # # On: perform on object

# # # Pipe: (->, ->>, as->)

# # # Resource: use context lib

# # # Context: pass dict

# # # Delay / Future

# # # Parallel

# # # Partial / Compose


# # def run(prog, state=None):
# #     for f, args, kwargs in prog.steps:
# #         state = f(*args, **kwargs)


# # def opt(prog, state=None, default=0):
# #     for f, args, kwargs in prog.steps:
# #         state = f(*args, **kwargs)

# #         if state is None:
# #             state = default


# # prog = Program((print, [0]))

# # with prog as steps:
# #     steps.append((print, [1, 2]))
# #     steps.append((print, [3, 4]))

# # run(prog)
