import math

def kullback_leibler_divergence(q_dist, p_dist, filter_by=0.001):
    assert len(q_dist) == len(p_dist)
    z = zip(q_dist, p_dist)
    divergence = 0.0
    for q, p in z:
        if q < filter_by and p < filter_by:
            continue
        if q > 0.0 and p > 0.0:
            divergence += q * math.log10(q / p)
    return divergence

def hellinger_distance(q_dist, p_dist, filter_by=0.001):
    assert len(q_dist) == len(p_dist)
    distance = 0.0
    z = zip(q_dist, p_dist)
    for q, p in z:
        if q < filter_by and p < filter_by:
            continue

        inner = math.sqrt(q) - math.sqrt(p)
        distance += (inner * inner)
    distance /= 2
    distance = math.sqrt(distance)
    return distance

def cosine_distance(q_dist,p_dist, filter_by=0.001):
    assert len(q_dist) == len(p_dist)
    z = zip(q_dist, p_dist)
    numerator = 0.0
    denominator_a = 0.0
    denominator_b = 0.0
    for q, p in z:
        if q < filter_by and p < filter_by:
            continue
        numerator += (q * p)
        denominator_a += (q * q)
        denominator_b += (p * p)
    denominator = math.sqrt(denominator_a) * math.sqrt(denominator_b)
    similarity = (numerator / denominator)
    return 1.0 - similarity


def jensen_shannon_divergence(q_dist, p_dist, filter_by=0.001):
    assert len(q_dist) == len(p_dist)
    z = zip(q_dist, p_dist)
    q_dist, p_dist, M = list(), list(), list()
    for q, p in z:
        if q < filter_by and p < filter_by:
            continue
        M.append((q + p) / 2)
        q_dist.append(q)
        p_dist.append(p)
    divergence_a = (kullback_leibler_divergence(q_dist,M) / 2)
    divergence_b = (kullback_leibler_divergence(p_dist,M) / 2)
    return divergence_a + divergence_b

def total_variation_distance(q_dist,p_dist, filter_by=0.001):
    z = zip(q_dist, p_dist)
    distance = 0.0
    for q, p in z:
        if q < filter_by and p < filter_by:
            continue
        distance += math.fabs(q - p)
    distance /= 2
    return distance
