FROM {{base_image}}
LABEL orchestrate-user-created=true

ADD "." "/"
WORKDIR /orchestrate

# Let the user set their pythonpath
{{#pythonpath}}
ENV PYTHONPATH "{{.}}"
{{/pythonpath}}

# Install the user's dependencies
{{#install_commands}}
RUN {{.}}
{{/install_commands}}
