from src.model.debt_dynamics import next_debt_ratio_exact, stabilising_primary

def test_stabilising_primary_keeps_debt_constant():
    d0, i, g = 1.0, 0.04, 0.03
    s_star = stabilising_primary(d0, i, g)
    d1 = next_debt_ratio_exact(d0, i, g, s_star)
    assert abs(d1 - d0) < 1e-12
