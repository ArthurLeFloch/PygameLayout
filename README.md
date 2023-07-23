# PygameLayout

This project was inspired by the way Android applications are designed and developed using Android Studio.
The objective is to avoid writing too much code for calculating the position of the elements on the screen,
and to provide an easy way to create a layout for a game or an application using some UI components.

UI components are taken from the [PygameUI](https://github.com/ArthurLeFloch/PygameUI) project, and can be installed using pip:
```bash
pip install pygame-ui-components
```

In order to keep the benefits of Pygame and the ability to draw whatever on screen, a new UI element has been created, named `View`.
This new element is actually a `Surface` from Pygame, and comes with a callback for each screen update.
This element should have more functionalities in the future, such as getting the mouse position on the surface.

This library uses XML files to generate a layout using UI components.

## Installation
```bash
pip install pygame-layout
```

## Examples
At the moment, the available examples are:
- [Overview](examples/overview/overview.py)
- [Password Generator](example/password_generator/password_generator.py)

In order to run an example, you must be in the same folder as the Python file.

## License
PygameLayout is licensed under the [GPL v3.0 License](LICENSE).
