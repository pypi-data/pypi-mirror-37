import igraph as ig
import leidenalg
#%%
G = ig.Graph.Erdos_Renyi(n=500, m=500)
#%%
part1 = leidenalg.find_partition(G, leidenalg.ModularityVertexPartition)
part2 = leidenalg.find_partition(G, leidenalg.ModularityVertexPartition)
print(part1.compare_to(part2, method='nmi'))
#%%

part1 = leidenalg.ModularityVertexPartition(G)
opt = leidenalg.Optimiser()
opt.set_rng_seed(0)
opt.optimise_partition(part1)

part2 = leidenalg.ModularityVertexPartition(G)
opt = leidenalg.Optimiser()
opt.set_rng_seed(0)
opt.optimise_partition(part2)
#%%
print(part1.compare_to(part2, method='nmi'))
