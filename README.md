# AutoPM: Automated Procurement Management

## Overview

AutoPM is a specialized application aimed at streamlining the procurement processes for funding agencies like the World Bank and African Development Bank (BAD), as well as State bodies. The core focus of AutoSPM is to deliver efficiency, fairness, and transparency in the procurement processes to ultimately achieve sustainable development and poverty reduction goals.

---

## Installation

### Prerequisites

- .NET 5.0 or higher

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/nyx-ei/autospm.git
    ```
    
2. Navigate to the project directory:
    ```bash
    cd AutoSPM
    ```

3. Restore NuGet packages:
    ```bash
    dotnet restore
    ```

4. Build and run the application:
    ```bash
    dotnet run
    ```

---

## Features

- Automated tender issuance and management
- Dashboard for real-time tracking of procurement processes
- Analytics for performance and fairness metrics
- Multi-level user roles for secure access control
- Transparent and secure document handling

---

## Usage

Refer to the [User Guide](docs/UserGuide.md) for a comprehensive overview on how to use AutoPM.

---

## Contributing

Contributions from the community are welcome! Please read our [Contributing Guide](docs/CONTRIBUTING.md) to get started.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- The World Bank
- African Development Bank (BAD)
- All other funding agencies and operational clients

---

For support or queries, feel free to reach out to us at help@nyx-ei.tech.

---

For any queries or support, please reach out to us at help@nyx-ei.tech

---
# Code conventions
## Namespaces
The universal namespace prefix is AutoSPM. For every class the namespace should respect this structure:
```
AutoSPM.funder.feature-family.feature.service
```
- **funder** is the funding organisation: WorldBank, African Bank for Development, ...
- **feature-family** is related to how the feature was designed.
- **feature** is the feature associated to your service.
- **service** is the service associated to your class.

_If you have any question related to namespaces convention, feel free to reach out to us at help@nyx-ei.tech._

---
# Architecture
