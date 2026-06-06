from typing import Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class Email:
    type: str
    format: str

    def __init__(self, type: str, format: str) -> None:
        self.type = type
        self.format = format

    @staticmethod
    def from_dict(obj: Any) -> 'Email':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        format = from_str(obj.get("format"))
        return Email(type, format)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["format"] = from_str(self.format)
        return result


class Username:
    type: str
    min_length: int

    def __init__(self, type: str, min_length: int) -> None:
        self.type = type
        self.min_length = min_length

    @staticmethod
    def from_dict(obj: Any) -> 'Username':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        min_length = from_int(obj.get("minLength"))
        return Username(type, min_length)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["minLength"] = from_int(self.min_length)
        return result


class Properties:
    id: Email
    username: Username
    email: Email

    def __init__(self, id: Email, username: Username, email: Email) -> None:
        self.id = id
        self.username = username
        self.email = email

    @staticmethod
    def from_dict(obj: Any) -> 'Properties':
        assert isinstance(obj, dict)
        id = Email.from_dict(obj.get("id"))
        username = Username.from_dict(obj.get("username"))
        email = Email.from_dict(obj.get("email"))
        return Properties(id, username, email)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = to_class(Email, self.id)
        result["username"] = to_class(Username, self.username)
        result["email"] = to_class(Email, self.email)
        return result


class User:
    title: str
    description: str
    type: str
    properties: Properties
    required: List[str]

    def __init__(self, title: str, description: str, type: str, properties: Properties, required: List[str]) -> None:
        self.title = title
        self.description = description
        self.type = type
        self.properties = properties
        self.required = required

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        title = from_str(obj.get("title"))
        description = from_str(obj.get("description"))
        type = from_str(obj.get("type"))
        properties = Properties.from_dict(obj.get("properties"))
        required = from_list(from_str, obj.get("required"))
        return User(title, description, type, properties, required)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_str(self.title)
        result["description"] = from_str(self.description)
        result["type"] = from_str(self.type)
        result["properties"] = to_class(Properties, self.properties)
        result["required"] = from_list(from_str, self.required)
        return result


def user_from_dict(s: Any) -> User:
    return User.from_dict(s)


def user_to_dict(x: User) -> Any:
    return to_class(User, x)
