#!/usr/bin/env python3

import os
from time import perf_counter_ns

class Value:
    def __init__(self, seed = None, filter = None, inverse_filter = None):
        self.lower = {
            'x': 1 if not seed else seed.lower['x'],
            'm': 1 if not seed else seed.lower['m'],
            'a': 1 if not seed else seed.lower['a'],
            's': 1 if not seed else seed.lower['s'],
        }
        self.upper = {
            'x': 4000 if not seed else seed.upper['x'],
            'm': 4000 if not seed else seed.upper['m'],
            'a': 4000 if not seed else seed.upper['a'],
            's': 4000 if not seed else seed.upper['s'],
        }        
        if filter:
            target, operator, value = filter
            if operator == '<':
                if self.upper[target] >= value:
                    self.upper[target] = value - 1
            elif operator == '>':
                if self.lower[target] <= value:
                    self.lower[target] = value + 1
        elif inverse_filter:
            target, operator, value = inverse_filter
            if operator == '<':
                if self.lower[target] < value:
                    self.lower[target] = value
            elif operator == '>':
                if self.upper[target] > value:
                    self.upper[target] = value
    
    def combinations(self):
        return (self.upper['x'] - self.lower['x'] + 1) * (self.upper['m'] - self.lower['m'] + 1) * (self.upper['a'] - self.lower['a'] + 1) * (self.upper['s'] - self.lower['s'] + 1)

    def is_valid(self):
        return self.lower['x'] <= self.upper['x'] and self.lower['m'] <= self.upper['m'] and self.lower['a'] <= self.upper['a'] and self.lower['s'] <= self.upper['s']

class Node:
    def __init__(self, input_value):
        self.input_value = input_value
        self.left_node = None
        self.left_value = None
        self.left_name = None
        self.right_node = None
        self.right_value = None
        
class Step:
    def __init__(self, data):
        if ':' not in data:
            self.target = data
            self.filter = None
        else:
            expression, self.target = data.split(':')
            self.filter = (expression[0], expression[1], int(expression[2:]))

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

    workflows, _ = data.split('\n\n')
    workflows = [Workflow(workflow) for workflow in workflows.split('\n')]  

    root = Node(Value())
    workflows_to_process = [('in', root)]

    answer = 0

    while workflow_to_process := workflows_to_process.pop(0) if workflows_to_process else False:
        current_workflow = Workflow.references[workflow_to_process[0]]
        current_node = workflow_to_process[1]
        
        for step in current_workflow.steps:
            current_node.left_name = step.target
            current_node.left_value = Value(seed = current_node.input_value, filter = step.filter)
            if step.target == 'A':
                answer += current_node.left_value.combinations()
            elif step.target == 'R':
                pass
            else:
                current_node.left_node = Node(current_node.left_value)
                workflows_to_process.append((step.target, current_node.left_node))
            if step.filter:
                current_node.right_value = Value(seed = current_node.input_value, inverse_filter = step.filter)
                current_node.right_node = Node(current_node.right_value)
            current_node = current_node.right_node

    end = perf_counter_ns()

    print(f'The answer is: {answer}')
    print(f'{((end-start)/1000000):.2f} milliseconds')

input_file = os.path.join(os.path.dirname(__file__), 'input')
answer(input_file)
