{%- if obj.ref_key is not none %}
.. _{{ obj.ref_key }}:
{% endif %}
{{ obj.title }}
{{ obj.header_char * obj._bar_length}}