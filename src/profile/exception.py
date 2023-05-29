from pydantic.errors import PydanticValueError


class InvalidImageType(PydanticValueError):
    code = "not_image"
    msg_template = "{msg}"


class ImageSizeTooBig(PydanticValueError):
    code = "big_size"
    msg_template = "{msg}"
