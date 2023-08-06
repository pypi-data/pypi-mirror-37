#!/usr/bin/env python
# coding: utf-8

# In[4]:


"""Structures of the project."""

from functools import reduce, partial
from itertools import chain, zip_longest

from typing import Union, Tuple, Mapping, Sequence, Iterable, Callable

from gampy.errors import DefinitionError, CompositionError


# In[13]:


# TYPES

Args = Sequence
Kwargs = Mapping
Function = Callable

Step = Tuple[Function, Args, Kwargs]
Advice = Callable[[Function], Function]
PartialStep = Union[Function, Sequence]


# In[17]:


class Pipeline:
    """A Pipeline is a sequence of steps."""

    def __init__(self, steps: Iterable) -> None:
        """Initialize object."""
        self._steps: list = []
        self.steps = steps  # trigger setter

    # OBJECT

    def __hash__(self) -> int:
        """Hash step functions."""
        functions = tuple(f for f, args, kwargs in self.steps)

        return hash(functions)

    # PROPERTY

    @property
    def steps(self) -> Sequence[Step]:
        """Get pipeline steps."""
        return self._steps

    @steps.setter
    def steps(self, steps: Iterable[PartialStep]) -> None:
        """Assign pipeline steps."""
        self._steps = []

        for s in steps:
            f = None
            args: list = list()
            kwargs: dict = dict()

            # fill blanks
            if callable(s):
                f = s
            elif isinstance(s, Sequence):
                if len(s) == 1:
                    f = s[0]
                elif len(s) == 2:
                    f = s[0]
                    args = s[1]
                elif len(s) == 3:
                    f = s[0]
                    args = s[1]
                    kwargs = s[2]
                else:
                    raise DefinitionError(
                        "A tuple step should contain 1, 2 or 3 items. Not: {}.".format(
                            len(s)
                        )
                    )
            else:
                raise DefinitionError(
                    "A step should be Callable or Iterable. Not: {}.".format(
                        type(s).__name__
                    )
                )

            # validate items
            if not callable(f):
                raise DefinitionError(
                    "The first step argument should be Callable. Not: {}.".format(
                        type(f).__name__
                    )
                )
            elif not isinstance(args, Args):
                raise DefinitionError(
                    "The second step argument should be Iterable. Not: {}.".format(
                        type(args).__name__
                    )
                )
            elif not isinstance(kwargs, Kwargs):
                raise DefinitionError(
                    "The third step argument should be Mapping. Not: {}.".format(
                        type(kwargs).__name__
                    )
                )

            step = (f, args, kwargs)
            self._steps.append(step)

    # CONTEXT

    def __enter__(self) -> Sequence[Step]:
        """Return steps in a context."""
        return self.steps

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Update steps from a context."""
        self.steps = self.steps  # trigger setter

    # OPERATION

    def __or__(self, f: Callable) -> "Pipeline":
        """Add a function step."""
        steps: list = list()
        steps.extend(self.steps)
        steps.append(f)

        return self.__class__(steps)

    def __and__(self, other: "Pipeline") -> "Pipeline":
        """Keep common steps."""
        steps = [s for s in self.steps if s in other.steps]

        return self.__class__(steps)

    def __xor__(self, other: "Pipeline") -> "Pipeline":
        """Keep uncommon steps."""
        return (self + other) - (self & other)

    def __add__(self, other: "Pipeline") -> "Pipeline":
        """Concatenate every steps."""
        steps: list = list()
        steps.extend(self.steps)
        steps.extend(other.steps)

        return self.__class__(steps)

    def __sub__(self, other: "Pipeline") -> "Pipeline":
        """Intersect common steps."""
        steps = [s for s in self.steps if s not in other.steps]

        return self.__class__(steps)

    def __mul__(self, n: int) -> "Pipeline":
        """Duplicate steps n times."""
        steps: list = []

        for _ in range(n):
            steps.extend(self.steps)

        return self.__class__(steps)

    def __matmul__(self, advice: Advice) -> "Pipeline":
        """Apply advice to step functions."""
        steps = [(advice(f), args, kwargs) for f, args, kwargs in self.steps]

        return self.__class__(steps)

    def __truediv__(self, n: int) -> Sequence["Pipeline"]:
        """Create step chunks of size n (strict)."""
        ps = []
        starts = range(0, len(self.steps), n)
        ends = range(n, len(self.steps) + n, n)

        for start, end in zip(starts, ends):
            steps = self.steps[start:end]
            pipe = self.__class__(steps)
            ps.append(pipe)

        return ps

    def __floordiv__(self, n: int) -> Sequence["Pipeline"]:
        """Create step chunks of size n (longest)."""
        ps = []
        ends = range(n, len(self.steps), n)
        starts = range(0, len(self.steps), n)

        for start, end in zip(starts, ends):
            steps = self.steps[start:end]
            pipe = self.__class__(steps)
            ps.append(pipe)

        return ps

    def __mod__(self, other: "Pipeline") -> "Pipeline":
        """Alternate between self and other steps."""
        gen = chain.from_iterable(zip_longest(self.steps, other.steps))
        steps = [s for s in gen if s is not None]

        return self.__class__(steps)

    # CONVERTION

    def __str__(self) -> str:
        """Return steps as a string."""
        return " -> ".join(f.__name__ for f, args, kwargs in self.steps)

    def __repr__(self) -> str:
        """Return steps as a raw string."""
        return str(self.steps)

    def __bool__(self) -> bool:
        """Return True if steps is not empty."""
        return len(self.steps) > 0

    def __call__(self) -> Callable:
        """Return a Callable through composition."""
        if not self.steps:
            raise CompositionError("Cannot compose from an empty pipeline.")

        def part(step):
            """Apply partial to one step."""
            f, args, kwargs = step
            h = partial(f, *args, **kwargs)

            return h

        def comp(f, g):
            """Apply compose to two steps."""

            def composition(*args, **kwargs):
                return g(f(*args, **kwargs))

            return composition

        functions = map(part, self.steps)
        function = reduce(comp, functions)

        return function

    # COLLECTION

    def __len__(self) -> int:
        """Return the number of steps."""
        return len(self.steps)

    def __iter__(self) -> Iterable[Step]:
        """Iterate over steps."""
        return iter(self.steps)

    def __getitem__(self, n: int) -> Step:
        """Return the nth step."""
        return self.steps[n]

    def __contains__(self, step: Step) -> bool:
        """Return True if step is in steps."""
        return step in self.steps

    def __reversed__(self) -> "Pipeline":
        """Reverse the order of steps."""
        return self.__class__(reversed(self.steps))

    # COMPARISON

    def __lt__(self, other: "Pipeline") -> bool:
        """Compare the step lengths with <."""
        return len(self) < len(other)

    def __gt__(self, other: "Pipeline") -> bool:
        """Compare the steps lengths with >."""
        return len(self) > len(other)

    def __le__(self, other: "Pipeline") -> bool:
        """Compare the step lengths with <=."""
        return len(self) <= len(other)

    def __ge__(self, other: "Pipeline") -> bool:
        """Compare the step lengths with >=."""
        return len(self) >= len(other)

    def __eq__(self, other) -> bool:
        """Compare the step lengths with ==."""
        return len(self.steps) == len(other.steps)

    def __ne__(self, other) -> bool:
        """Compare the step lengths with !=."""
        return len(self.steps) != len(other.steps)

    def __pow__(self, other: "Pipeline") -> bool:
        """Compare the pipeline functions in order."""
        fself = [f for f, args, kwargs in self.steps]
        fother = [f for f, args, kwargs in other.steps]

        return fself == fother

    def __lshift__(self, other: "Pipeline") -> bool:
        """Return True if self is a subset of other."""
        for s in self.steps:
            if s not in other.steps:
                return False

        return True

    def __rshift__(self, other: "Pipeline") -> bool:
        """Return True if self is a superset of other."""
        for s in other.steps:
            if s not in self.steps:
                return False

        return True
