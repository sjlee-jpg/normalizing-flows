import numpy as np
import torch
import torch.nn as nn

def divergence_exact(output, input):
    diag = torch.zeros_like(input)
    for i in range(input.shape[-1]):
        diag[...,i] += torch.autograd.grad(output[...,i].sum(), input, create_graph=True)[0].contiguous()[...,i].contiguous()
    return diag

def divergence_exact_for_sets(output, input):
    diag = torch.zeros_like(input)
    for i in range(input.shape[-2]):
        for j in range(input.shape[-1]):
            diag[...,i,j] += torch.autograd.grad(output[...,i,j].sum(), input, create_graph=True)[0].contiguous()[...,i,j].contiguous()
    return diag

def divergence_approx(output, input, e, samples=1):
    out = 0
    for _ in range(samples):
        out += torch.autograd.grad(output, input, e, create_graph=True)[0] * e / samples
    return out

def divergence_from_jacobian(f, inputs):
    """ Calculates exact divergence for any input shape.
    Args:
        f: (callable) function that transforms a single or tuple of inputs to an output of same size
        inputs: (tensor) or (tuple of tensors)
    """
    if not isinstance(inputs, tuple):
        inputs = (inputs,)
    jac = torch.autograd.functional.jacobian(f, inputs)
    div = tuple(torch.diag(d.view(np.prod(x.shape), -1)).view(*x.shape) for d, x in zip(jac, inputs))
    if len(div) == 1:
        div = div[0]
    return div
