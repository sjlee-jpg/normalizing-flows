import pytest
import nf
import torch

@pytest.mark.parametrize('dim', [2, 3, 11])
@pytest.mark.parametrize('latent_dim', [1, 3, 8])
def test_mlp_zero_trace(dim, latent_dim):
    torch.manual_seed(123)

    out_dim = dim * latent_dim
    model = nf.net.DiffeqZeroTraceMLP(dim, [64, 64], out_dim)

    t = torch.Tensor([1])
    x = torch.randn(10, dim)
    y, jac = model(t, x)

    assert y.shape[:-1] == x.shape[:-1] and y.shape[-1] == out_dim

    f = lambda t, x: model(t, x)[0]
    jac_exact = nf.util.divergence_from_jacobian(f, (t, x))[1]

    assert jac_exact.sum() == 0
    assert torch.isclose(jac_exact, jac).all()

@pytest.mark.parametrize('dim', [2, 3, 11])
@pytest.mark.parametrize('latent_dim', [1, 3, 8])
def test_deepset_zero_trace(dim, latent_dim):
    torch.manual_seed(123)

    out_dim = dim * latent_dim
    model = nf.net.DiffeqZeroTraceDeepSet(dim, [64, 64], out_dim, pooling='max')

    t = torch.Tensor([1])
    x = torch.randn(5, 10, dim)

    y, jac = model(t, x)

    assert len(y) == len(x) and y.shape[:-1] == x.shape[:-1] and y.shape[-1] == out_dim

    f = lambda t, x: model(t, x)[0]
    jac_exact = nf.util.divergence_from_jacobian(f, (t, x))[1]

    assert jac_exact.sum() == 0
    assert torch.isclose(jac_exact, jac).all()

@pytest.mark.parametrize('input_dim', [(2, 5, 7), (3, 4, 5, 2)])
@pytest.mark.parametrize('latent_dim', [1, 8])
@pytest.mark.parametrize('n_heads', [1, 2])
def test_attention_zero_trace(input_dim, latent_dim, n_heads):
    torch.manual_seed(123)

    dim = input_dim[-1]
    model = nf.net.DiffeqZeroTraceAttention(dim, [64, 64], dim * latent_dim, n_heads=n_heads)

    t = torch.Tensor([1])
    x = torch.randn(*input_dim)

    y, jac = model(t, x)
    f = lambda t, x: model(t, x)[0]
    jac_exact = nf.util.divergence_from_jacobian(f, (t, x))[1]

    assert jac_exact.sum() == 0
    assert torch.isclose(jac, jac_exact).all()
