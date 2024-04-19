import streamlit as st

st.set_page_config(layout="wide")

# introduction
st.title("🏠 Home Page")
st.write("## Welcome to the Logistics Algorithm Testing")
st.write("This application is designed to test different algorithms for loading items into containers. The app will include an interface to allow the user to select the container, select the mission type, then filter the items to be packed. The app will then display the bin packing results.")
st.write("**Please select a page from the sidebar to get started.**")

st.divider()

# aglorithm descriptions
st.write("### Algorithms/Implementations")
st.write("1. Bin Packing - The bin packing problem is a classic optimization problem where the goal is to efficiently pack objects of varying sizes into a finite number of bins or containers of a fixed capacity in a way that minimizes the number of bins used. It is often used in fields such as logistics, manufacturing, and computer science, especially in resource allocation and data organization contexts.")
st.write("2. Network Flow - Network flow is a fundamental concept in operations research and computer science, dealing with the flow of items through a network of interconnected nodes or points. This concept is typically visualized as directed graphs where nodes represent distribution points, and edges represent the paths or channels along which items (like data, resources, or commodities) can flow. The primary goal in network flow problems is to determine the optimal way to route these items from one or more sources to one or more sinks (destinations) while satisfying certain constraints.")

tab1, tab2, tab3, tab4 = st.tabs(["Bin Packing Strengths", "Bin Packing Weaknesses", "Network Flow Strengths", "Network Flow Weaknesses"])

with tab1:
    st.write("##### Bin Packing Strengths")
    st.write("1. **Resource Optimization:** Bin packing algorithms are designed to minimize waste, whether that waste is space in shipping containers, memory in computer storage, or time slots in scheduling problems. This leads to cost savings and increased efficiency in operations.")
    st.write("2. **Flexibility and Applicability:** There are many variations and extensions to the basic bin packing problem that can accommodate a range of constraints and real-world considerations. This makes it adaptable to a wide variety of situations.")
    st.write("3. **Algorithmic Variety:** There are multiple algorithms available for tackling bin packing problems, ranging from exact solutions to heuristic and approximation algorithms. This variety allows for choosing an approach that best fits the specific needs and trade-offs of a scenario, such as computational complexity versus accuracy.")
    st.write("4. **Scalability with Heuristics:** TFor large-scale problems, heuristic methods like First-Fit, Best-Fit, and Genetic Algorithms can provide good-enough solutions relatively quickly and scale well, even though they may not guarantee the best solution.")

with tab2:
    st.write("##### Bin Packing Weaknesses")
    st.write("1. **NP-Completeness:** The bin packing problem is NP-complete, which means there is no known algorithm that can find an optimal solution efficiently (in polynomial time) for all possible inputs. This complexity implies that as the size of the problem increases, the time required to find the exact solution can grow exponentially.")
    st.write("2. **Approximation and Heuristics Limitations:** While heuristic methods can solve problems quickly, they often do not guarantee an optimal solution. The quality of the solution can vary significantly based on the specifics of the data and the heuristic used. In some cases, these methods might lead to significantly suboptimal solutions.")
    st.write("3. **Sensitivity to Item Sizes and Order:** The performance and effectiveness of certain bin packing algorithms can be highly sensitive to the order in which items are packed and their sizes. Some algorithms might perform well on uniformly sized items but poorly on heterogeneous item sizes.")
    st.write("4. **Complexity in Configuration:** Configuring bin packing algorithms to deal with additional real-world constraints (like weight limits, different shapes, or specific stacking rules) can significantly increase the complexity of the problem. This may require custom solutions or adaptations, increasing development time and computational resources.")

with tab3:
    st.write("##### Network Flow Strengths")
    st.write("1. **Optimal Resource Distribution:** Network flow algorithms excel at finding the optimal way to distribute resources across a network, maximizing throughput and efficiency, such as maximizing the amount of data that can be sent through a network or maximizing the delivery of goods across logistics networks.")
    st.write("2. **Wide Range of Applications:** These algorithms can be applied to various fields such as telecommunications, transportation, supply chain management, and even in financial modeling (like cash flow optimization).")
    st.write("3. **Well-Established Algorithms:** There are several robust and well-tested algorithms for solving network flow problems, such as Ford-Fulkerson, Edmonds-Karp, and Dinic's Algorithm. These are based on solid mathematical foundations and can provide exact solutions.")
    st.write("4. **Multiple Variants:** Beyond simple max-flow problems, network flow algorithms can handle more complex scenarios including multi-commodity flows (different items flowing through the network), minimum cost flows (finding the cheapest way to satisfy flow requirements), and flow with lower bounds (each edge must have at least a certain amount of flow).")

with tab4:
    st.write("##### Network Flow Weaknesses")
    st.write("1. **Complexity in Large Networks:** While polynomial-time algorithms exist for network flow problems, the actual time and space complexity can still be prohibitive for very large networks with many nodes and edges.")
    st.write("2. **Static Models:** Traditional network flow models are static; they do not inherently account for changes over time in the network's state or capacities. Dynamic network flow models exist but are significantly more complex and computationally intensive.")
    st.write("3. **Assumption of Homogeneity:** Basic network flow models often assume that the items flowing through the network are homogeneous and divisible. This can limit their applicability in situations where the items are heterogeneous (different types of commodities) or indivisible without adaptations to the model.")
    st.write("4. **Sensitivity to Network Topology and Capacity Changes:** The solutions can be highly sensitive to changes in network topology (such as adding or removing nodes and edges) and edge capacities. Small changes in these parameters can lead to significantly different flow distributions.")

with st.expander("References"):
    st.write("1. [Bin Packing Problem](https://en.wikipedia.org/wiki/Bin_packing_problem)")
    st.write("2. [Network Flow Problem](https://en.wikipedia.org/wiki/Maximum_flow_problem)")