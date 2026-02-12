from typing import TypedDict, Union, Optional, Any


# typed dictionary
class Movie(TypedDict):
    title: str
    year: int
    rating: float


movie: Movie = {
    "title": "The Dark Knight",
    "year": 2008,
    "rating": 9.0
}
movie1 = Movie(title="The Dark Knight", year=2008, rating=9.0)
print(movie)
print(movie1)

# Union


def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    return a + b


print(add(1, 2))
print(add(1.0, 2.0))

# Optional


def add(a: Optional[int] = None, b: Optional[int] = None) -> Optional[int]:
    if a is None or b is None:
        return None
    return a + b


print(add(1, 2))

# Any


def add(a: Any, b: Any) -> Any:
    return a + b


print(add(1, 2))
print(add(1.0, 2.0))
print(add("Hello", "World"))


# lambda functions
num = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x*x, num))
print(squares)
