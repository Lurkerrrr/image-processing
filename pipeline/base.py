from PIL import Image


def filter_step(name: str):
    """Decorator that marks a function as a named pipeline filter step."""
    def decorator(func):
        func._is_filter = True
        func._filter_name = name
        return func
    return decorator


class PipelineMeta(type):
    """
    Metaclass that automatically discovers and registers all methods
    marked with the @filter_step decorator when a class is created.
    """
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        cls._registry = {}

        for attr_name, attr_value in namespace.items():
            if callable(attr_value) and getattr(attr_value, "_is_filter", False):
                filter_name = attr_value._filter_name
                cls._registry[filter_name] = attr_value
                print(f"[PipelineMeta] Registered filter: '{filter_name}'")

        return cls


class ImagePipeline(metaclass=PipelineMeta):
    """
    Base class for the image processing pipeline.
    Subclasses define filters using @filter_step decorator.
    The metaclass automatically registers them.
    """

    def run(self, image: Image.Image, steps: list[str]) -> Image.Image:
        """
        Run the pipeline by applying the requested filter steps in order.

        :param image: Input PIL Image
        :param steps: List of filter names to apply in order
        :return: Processed PIL Image
        """
        for step in steps:
            if step not in self._registry:
                print(f"[Pipeline] Warning: filter '{step}' not found, skipping.")
                continue
            print(f"[Pipeline] Applying filter: '{step}'")
            image = self._registry[step](self, image)
        return image