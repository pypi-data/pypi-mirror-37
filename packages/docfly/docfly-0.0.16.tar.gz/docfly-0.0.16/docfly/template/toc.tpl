.. toctree::
    :maxdepth: {{ maxdepth }}

    {% for article in article_list -%}
    {{ article.title }} <{{ article.rel_path }}>
    {% endfor -%}
