=======
arachno
=======

Utility to orchestrate coroutines via DSL.

Example
-------

.. code-block:: js

    {
        "actions": {
            "target": {
                "operation": "search-api.get_product",
                "args": {
                    "product_id": "${product_id}"
                },
                "defines": {
                    "product-category": "result.category",
                    "product-price": "result.price"
                },
                "options": {
                    "timeout": "1s"
                }
            },
            "target-account": {
                "operation": "accounts-repository.get",
                "args": {
                    "account_id": "${account_id}"
                },
                "defines": {
                    "favorite-categories": "${account.favorite-categories}"
                },
                "options": {
                    "timeout": "1s"
                }
            },
            "product-selector": {
                "operation": "product-stats.calculate_params",
                "args": {
                    "input": {
                        "category": "${target.product-category}",
                        "country": "${target.product-price}",
                        "segment": "Germany"
                    },
                    "jitter_percent": 10
                },
                "defines": {
                    "output-args": "value"
                }
            },
            "similar-products": {
                "operation": "search-api.search",
                "args": {
                    "product_codes": "${product-selector.output-args}",
                    "categories": {
                        "oneof": "${target-account.favorite-categories}"
                    }
                },
                "options": {
                    "timeout": "600ms"
                }
            }
        }
    }