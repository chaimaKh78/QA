# fix_template.py
import os

BASE = r'D:\NouvelairApp\nouvelair_project'
tmpl = os.path.join(BASE, 'flights', 'templates', 'flights', 'home.html')

with open(tmpl, 'r', encoding='utf-8') as f:
    content = f.read()

# Add error display block right after <form> tag
old = '''<form method="post" action="{% url 'flights:home' %}">
                        {% csrf_token %}'''

new = '''<form method="post" action="{% url 'flights:home' %}">
                        {% csrf_token %}
                        {% if search_form.non_field_errors %}
                        <div class="alert alert-danger">
                            {% for error in search_form.non_field_errors %}
                            {{ error }}
                            {% endfor %}
                        </div>
                        {% endif %}'''

content = content.replace(old, new)

with open(tmpl, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Added non_field_errors display to home.html")