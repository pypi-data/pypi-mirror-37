FROM {{base_image}}

ADD "." "/"

# Let the user set their pythonpath
{{#pythonpath}}
ENV PYTHONPATH "{{.}}"
{{/pythonpath}}

# Install the user's dependencies
{{#install_commands}}
RUN {{.}}
{{/install_commands}}
