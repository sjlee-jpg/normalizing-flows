import pytest
import nf
import torch

@pytest.mark.parametrize('input_dim', [(1, 1, 1), (10, 3, 2), (5, 3, 2, 3), (10, 11, 13, 23, 37)])
@pytest.mark.parametrize('hidden_dims', [[32], [64, 32]])
@pytest.mark.parametrize('out_dim', [1, 2, 5])
@pytest.mark.parametrize('n_heads', [1, 4, 8])
@pytest.mark.parametrize('mask_diagonal', [True, False])
def test_attention_equivariance_and_masking(input_dim, hidden_dims, out_dim, n_heads, mask_diagonal):
    torch.manual_seed(123)

    model = nf.net.Attention(input_dim[-1], hidden_dims, out_dim, n_heads, mask_diagonal)

    x = torch.randn(*input_dim)
    y = model(x, x, x)

    # Check if permutation equivariant
    x_flip = torch.flip(x, [-2])
    y_flip = model(x_flip, x_flip, x_flip)
    y_flip = torch.flip(y_flip, [-2]) # Flip back to original order

    assert torch.isclose(y, y_flip, atol=1e-5, rtol=1e-5).all(), 'Attention should be permutation invariant'

    # Check if masking works
    mask = torch.rand(*input_dim[:-1], 1).round()
    mask[...,0,0] = 1 # Make sure at least one element is not masked
    y = model(x, x, x, mask)
    x_perm = x + x * (1 - mask) * torch.rand(*input_dim)
    y_perm = model(x_perm, x_perm, x_perm, mask)

    assert torch.isclose(y, y_perm, atol=1e-5, rtol=1e-5).all(), 'Masking in attention doesn\'t work'
