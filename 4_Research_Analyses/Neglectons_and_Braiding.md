# Neglectons & Braiding

## Research Context
Topological quantum computation (TQC) encodes quantum information in non-local degrees of freedom associated with quasiparticles exhibiting non-Abelian exchange statistics. The resulting unitary evolution depends only on the topology of braiding worldlines, rather than on local dynamical fluctuations, enabling intrinsic fault tolerance [1], [2].

A prominent physical platform is the fractional quantum Hall (FQH) state at filling factor $\nu = 5/2$, where the Moore–Read (Pfaffian) phase predicts quasiparticles described by the Ising modular tensor category [1], [2]. The topological charges:

$$
{1, \sigma, \psi}
$$

satisfy fusion rules including:

$$
\sigma \times \sigma = 1 + \psi
$$

Braiding these excitations implements Clifford operations protected from local noise, but **Ising braiding alone is not universal**—it generates only a finite image of the braid group, requiring magic-state distillation for full computational power [2].

### Non-Semisimple Extensions and Neglectons
Recent advancements propose generalizing the Ising theory using non-semisimple topological quantum field theories (TQFTs), in which objects with vanishing quantum dimension—normally discarded under semisimplification—are retained via modified or renormalized quantum traces. These objects form indecomposable representations and include a new excitation class referred to as neglectons [3], [4].

Semisimple constructions restrict allowed objects to direct sums of simple modules, with diagonalizable fusion and braiding. By contrast, non-semisimple representations may:
- be reducible but not decomposable,
- exhibit Jordan block structure,
- introduce non-diagonalizable braiding matrices,
- and modify the topological inner product to have mixed signature.

In this generalized setting, the set of topological charges expands beyond ${1,\sigma, \psi}$ to include a continuous family of neutral excitations parameterized by a real index $\alpha$. These excitations possess formal quantum dimension zero yet acquire physical significance through altered trace definitions that couple them to the computational subspace [3].

### Computational Motivation
Semisimple Ising anyon systems implement only Clifford operations under braiding, as their braid group representations have finite image and cannot approximate arbitrary rotations. As a result, universal quantum computation requires additional non-topological resources, typically magic-state distillation or projective measurements, which dominate hardware overhead in Ising–Majorana platforms [2], [5].

Non-semisimple extensions modify the braid group action by introducing indecomposable excitations that promote the ordinary braid group $B_n$ to affine braid representations, enabling continuously parameterized unitary gates. This restores universality under braiding alone, removing the need for magic-state distillation and aligning computational power with that of models such as Fibonacci anyons—while preserving ties to experimentally supported Ising platforms [4], [6].

Thus, neglectons offer a middle ground between theoretical universality and practical feasibility:  

- broader computational expressivity than semisimple Ising models  
- lower physical overhead than distillation-based schemes  
- and greater experimental plausibility than Fibonacci-based models


### Scope of This Analysis
This research analysis synthesizes findings on:
- the mathematical structure of neglectons within non-semisimple TQFTs [1], [3],
- their impact on fusion, braiding, and universality [4],
- numerical compilation of universal gate sets [6],
- and conceptual extensions relating to cognition as proposed by speculative literature [7].

External citations are included only where historically and scientifically necessary to contextualize well-established aspects of TQC (e.g., Ising anyons in $\nu = 5/2$ QH systems [2]).

The subsequent sections expand on theoretical insights, mathematical foundations, computational implications, and open problems in this emerging framework.

---

## Key Insights
### Neglectons Extend the Ising Fusion Theory
Neglectons emerge when trace-zero objects removed during semisimplification are retained via renormalized quantum traces. They expand the set of topological charges beyond ${1, \sigma, \psi\}$ to a parameterized family $\alpha \in \mathbb{R}$ [3], [4].

A representative extended fusion rule:

$$
\alpha \times \sigma = (\alpha + 1) \oplus (\alpha - 1)
$$

Fusion no longer decomposes into simples, enabling richer multi-channel state evolution.

### Universality via Affine Braiding
Fixing a neglecton introduces a puncture in the topological plane, promoting the braid group from:

$$
B_n \rightarrow \text{Aff}(B_n)
$$

This allows continuous families of braid representations dense in $SU(2)$, restoring universality for suitable $\alpha$ values [4].

By contrast:

- Semisimple Ising $\rightarrow$ Clifford only
- Fibonacci $\rightarrow$ universal but not experimentally verified
- Neglecton-Ising $\rightarrow$ universal *and plausibly physical*

### Numerical Gate Synthesis
Monte Carlo–enhanced Solovay–Kitaev compilation using elementary braiding matrices yields efficient approximations of:

- $H$-gate
- $T$-gate
- $CNOT$

with shallow recursion depth $(\leq 3)$ [6].

This provides operational support for universal computation without auxiliary non-topological resources.

### Relation to $\nu = 5/2$ Physics
Ising anyons already appear in experimental signatures of the $\nu = 5/2$ FQH state. Neglectons may emerge as refinements of these phases through altered edge conditions, symmetry breaking, or engineered defects [3], [4].

---

## Analytical Commentary
### Semisimplification vs. Non-Semisimple Reconstruction
Semisimple Ising TQFT discards representations with $\text{qdim} = 0$ to maintain modularity. Non-semisimple extensions retain them using renormalized traces:

$$
\text{tr}_R(X) \neq 0 \quad \text{even if} \quad \text{qdim}(X)=0
$$

resulting in **indecomposable but reducible** objects [3].

### Mixed-Signature Hilbert Spaces
Neglecton-based Hilbert spaces may take the form:

$$
\mathcal{H} \cong \mathbb{C}^{p,q}
$$

with both positive- and negative-norm sectors. Computation requires isolating a positive-definite subspace:

$$
\mathcal{H}_{\text{comp}} \subset \mathcal{H}
$$

for certain $\alpha$, decoupling from unphysical leakage channels [4].

### Hierarchical Fusion Channels
Neglectons are organized in chains:

$$
\alpha \leftrightarrow \alpha \pm 1
$$

inducing layered fusion spaces with internal morphisms rather than direct sums of simples [3].

### Affine Braid Representations
Affine braiding introduces continuously parameterized matrices rather than fixed Clifford transformations, permitting dense coverage of $SU(2)$ [4].

---

## Future Directions
- **Physical realization of non-semisimple phases**: Develop Hamiltonians or engineered topological media that realize neglectons as quasiparticles rather than purely categorical constructs, including modified boundary conditions in $\nu = 5/2$ systems and hybrid Majorana platforms [3], [4].

- **Fault-tolerance in mixed-signature spaces**: Define noise models, stabilizer analogues, and threshold conditions when computational subspaces coexist with indefinite inner products [4].

- **Resource comparison vs. magic-state architectures**: Benchmark braid depth, coherence requirements, and error rates relative to Clifford+T and Fibonacci qubits; early evidence suggests efficient compilation [6].

- **Classifying the $\alpha$-parameter family**: Map universality domains, unitarity conditions, and anomaly-free parameter ranges connecting neglectons to logarithmic CFT structures [3].

- **Observable signatures**:  Establish measurable consequences, such as altered tunneling conductance, modified quasiparticle statistics, or entanglement-spectrum deviations.

---

## Speculative Extensions (Not Supported by Empirical Evidence)
- **Bulk–boundary separation as persistent internal state**: Indecomposable internal sectors have been analogized to persistent memory or identity structures in cognitive systems; such claims are conceptual, without evidence [7].

- **Affine braiding as irreversible information flow**: Non-contractible holonomies have been interpreted metaphorically as long-range memory traces; no physical support exists [7].

- **Cayley cubic singularities and cognitive depth**: Parabolic singularities in the modified moduli space have been linked philosophically to cognitive asymmetry, not experimentally or theoretically validated [7].

- **Scope restriction**: This document treats neglectons strictly as topological excitations relevant to quantum computation, not cognitive architecture.

---

## References

[1] Moore, G. W., & Read, N. W. (1991). Nonabelions in the fractional quantum hall effect. 360(2-3), 362–396. https://doi.org/10.1016/0550-3213(91)90407-o

[2] Nayak, C., Simon, S. H., Stern, A., Freedman, M., & Das Sarma, S. (2008). Non-Abelian anyons and topological quantum computation. Reviews of Modern Physics, 80(3), 1083–1159. https://doi.org/10.1103/revmodphys.80.1083

[3] Iulianelli, F., Kim, S., Sussan, J., & Lauda, A. D. (2025). From negligible to neglecton: making Ising anyons braiding universal. arXiv preprint arXiv:2509.02843.

[4] Iulianelli, F., Kim, S., Sussan, J., & Lauda, A. D. (2025). Universal quantum computation using Ising anyons from a non-semisimple topological quantum field theory. Nature Communications, 16(1). https://doi.org/10.1038/s41467-025-61342-8

[5] Kitaev, A. Yu. (2003). Fault-tolerant quantum computation by anyons. Annals of Physics, 303(1), 2–30. https://doi.org/10.1016/S0003-4916(02)00018-0

[6] Long, J., Li, Y., Zhong, J., & Meng, L. (2025). Topological quantum compilation for non-semisimple Ising anyons via monte carlo simulations. arXiv preprint arXiv:2511.13194.

[7] Planat, M. (2025). Murakamian Ombre: Non-Semisimple Topology, Cayley Cubics, and the Foundations of a Conscious AGI.
