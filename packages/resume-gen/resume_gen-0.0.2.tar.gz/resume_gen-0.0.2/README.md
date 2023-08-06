# Resume Generator
## Install
```commandline
pip install resume_gen
```
## Example
Here's an example of building a PDF resume from JSON data and a template.
- [Template](examples/simple/simple_template.tex)
- [JSON Data](examples/simple/charles_babbage.json)
- [Output PDF](examples/simple/Charles_Babbage.pdf)
```python
from resume_gen import Person, ResumeTemplate, ResumeGenerator
import json

# Build a resume generator
resume_generator = ResumeGenerator()

# Build the template for the resume
template = ResumeTemplate('simple_template.tex')

# Load the Charles Babbage data from the JSON file
with open('charles_babbage.json') as people_file:
    charles_babbage_json = json.load(people_file)

# Build a person from JSON
person = Person.from_json(charles_babbage_json)

# Generate and save the resume
resume_generator.generate(
    template,
    person,
    '{}_{}.pdf'.format(person.first_name, person.last_name))
```
