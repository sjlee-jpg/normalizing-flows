import pytest
import nf
import torch

@pytest.mark.parametrize('input_dim', [(10, 2), (2, 10), (1, 10, 2), (5, 10, 2)])
@pytest.mark.parametrize('natural_ordering', [True, False])
@pytest.mark.parametrize('reverse_ordering', [True, False])
@pytest.mark.parametrize('return_per_dim', [True, False])
def test_made_zero_trace(input_dim, natural_ordering, reverse_ordering, return_per_dim):
    torch.manual_seed(123)

    dim = input_dim[-1]
    model = nf.net.MADE(dim, [64, 64], dim * 8,
                        natural_ordering=natural_ordering,
                        reverse_ordering=reverse_ordering,
                        return_per_dim=return_per_dim)

    x = torch.randn(*input_dim).requires_grad_(True)

    f = lambda x: model(x)
    trace_exact = nf.util.divergence_from_jacobian(f, x)

    assert trace_exact.sum() == 0
