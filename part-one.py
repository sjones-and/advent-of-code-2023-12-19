#!/usr/bin/env python3

import os
from time import perf_counter_ns
from json import loads

class Step:
    def __init__(self, data):
        if ':' not in data:
            self.target = data
            self.subject = 'x'
            self.test = lambda i: True
        else:
            expression, self.target = data.split(':')
            self.subject = expression[0]
            if expression[1] == '<':
                self.test = lambda i: i < int(expression[2:])
            elif expression[1] == '>':
                self.test = lambda i: i > int(expression[2:])
            else:
                assert(False)

    def evaluate(self, subject):
       return self.target if self.test(subject[self.subject]) else None


class Workflow:
    references = {}

    def __init__(self, data):
        self.name, definition = data.split('{')
        self.steps = [Step(step) for step in definition.strip('}').split(',')]
        Workflow.references[self.name] = self

def answer(input_file):
    start = perf_counter_ns()
    with open(input_file, 'r') as input:
        data = input.read()

    workflows, shapes = data.split('\n\n')
    workflows = [Workflow(workflow) for workflow in workflows.split('\n')]  
    shapes = [loads(shape.replace('x','"x"').replace('m','"m"').replace('a','"a"').replace('s','"s"').replace('=',':')) for shape in shapes.split('\n')]

    accepted_shapes = []
    for shape in shapes:
        steps_to_process = [step for step in Workflow.references['in'].steps]
        while step := steps_to_process.pop(0) if steps_to_process else False:
            next = step.evaluate(shape)
            if not next:
                continue
            if next == 'A':
                accepted_shapes.append(shape)
                break
            elif next == 'R':
                break
            else:
                steps_to_process = [step for step in Workflow.references[next].steps]

    answer = sum([sum(shape.values()) for shape in accepted_shapes])
    end = perf_counter_ns()

    print(f'The answer is: {answer}')
    print(f'{((end-start)/1000000):.2f} milliseconds')

input_file = os.path.join(os.path.dirname(__file__), 'input')
answer(input_file)
