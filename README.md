For your GitHub repository with the described structure and file contents, here is a sample `README.md` that you can use. This README includes an introduction to the project, descriptions of the main components, and instructions for setting up and running the application.

# Logistics Algorithm Testing Application

This application is designed to test different algorithms for loading items into containers, utilizing Streamlit for an interactive UI. It allows users to select containers, choose mission types, and then filter and pack items according to two main algorithms: Bin Packing and Network Flow.

## Repository Structure
```
Main/
├── pages/
│   ├── 🌐_network_flow.py  # Handles network flow simulations
│   ├── 📦_bin_packing.py   # Manages bin packing simulations
│   └── functions/
│       ├── bp_func.py      # Bin packing utility functions
│       └── nflow.py        # Network flow utility functions
├── cost_estimates.csv      # CSV file with data for simulations
└── 🏠_home.py              # Streamlit interface for the home page
```

## Features

- **Bin Packing**: Optimizes the placement of objects of varying sizes into a limited number of bins or containers to minimize the space wasted.
- **Network Flow**: Manages the flow of items through a network, optimizing the routing from sources to sinks under various constraints.
- **Interactive Web UI**: Built with Streamlit, this application provides an intuitive user interface to interact with the algorithms.

## Getting Started

### Prerequisites

You need to have Python installed on your machine along with Streamlit. You can install Streamlit using pip:

```bash
pip install streamlit
```

### Running the Application

1. Clone this repository to your local machine.
2. Navigate to the directory containing the cloned files.
3. Run the application using Streamlit:

```bash
streamlit run 🏠_home.py
```

This will start a local web server and open the application in your default web browser.

## Usage

- **Select a Container**: Choose a container based on the mission requirements.
- **Choose Mission Type**: Filter the items by selecting the appropriate mission type.
- **Item Packing**: Visualize how items are packed within the containers using the Bin Packing algorithm.
- **Network Flow Simulation**: View the network flow graph and results, illustrating the optimal routing of items.

## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your enhancements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```

Feel free to adjust the content as needed to better fit the specifics of your project or to expand on certain sections with more detailed explanations or additional sections such as 'Troubleshooting', 'Future Work', etc.