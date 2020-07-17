# takes a list of bad inputs and removes from all inputs.
# returns only a list of good inputs that have a unique min set

def remove_bad_inputs(all_inputs, bad_inputs):
    for input in bad_inputs:
        all_inputs.remove(input)
