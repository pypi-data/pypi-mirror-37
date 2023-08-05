# Configurable LTI Consumer XBlock

This XBlock is used to replace edX's lti_consumer xblock. It makes available to
conceptors in CMS several preconfigured versions of LTI Consumer original
XBlock. Preconfigured fields are no longer modifiable.

## Installation

This package can be installed with `pip`:

```bash
$ pip install [--process-dependency-links] configurable_lti_consumer-xblock
```

Note that the `--process-dependency-links` `pip` option is only required to
install or test this Xblock as a standalone package. If you plan to install it
in a base Open edX installation, then you can safely miss this option as the
only package dependency should already have been resolved.

## Configuration example

The below example configuration instanciate 2 xblocks.

```python
CONFIGURABLE_XBLOCKS_SETTINGS = {
    "components": [{
        "module": "lti_consumer",
        "base_class": "ConfigurableLtiConsumerXBlock",
        "subclasses": [{
            "name": "Demo LTI Service",
            "display": "Demo LTI xblock",
            "lti": {
                "key": "jisc.ac.uk",
                "secret": "secret",
            },
            "default_values": {
                "description": "Demo",
                "lti_id": "",
                "launch_target": "iframe",
                "launch_url": "http://ltiapps.net/test/tp.php",
                "custom_parameters": [],
                "button_text": "button",
                "inline_height": 800,
                "modal_height": 800,
                "modal_width": 80,
                "has_score": False,
                "weight": 0,
                "hide_launch": False,
                "accept_grades_past_due": False,
                "ask_to_send_username": True,
                "ask_to_send_email": True

            }
        },{
            "name": "Generic",
            "display": "Generic LTI xblock",
            "default_values": {
                "description": "Generic",
                "ask_to_send_username": True,
                "ask_to_send_email": True
            }
        }]
    }]
}
```

You also need to set XBLOCK_SELECT_FUNCTION setting to enforce
configurable_lti_consumer endpoint over lti_consumer's one.

```python
try:
    from configurable_lti_consumer import configurable_xblocks
    XBLOCK_SELECT_FUNCTION = configurable_xblocks
except ImportError:
    pass
```

## Studio integration

For now studio integration is made by inserting `utils.configurable_xblocks`
function call in `edx-platform/cms/djangoapps/contentstore/views/component.py`.
It adds to preconfigured xblocks "Advanced" button.
