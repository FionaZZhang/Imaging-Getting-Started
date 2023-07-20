# Democratising-Imaging

This repo will contain introductory wiki for the [Imaging Project](https://wehi-researchcomputing.github.io/student-imaging). This wiki serves as a central hub for documentation, guides, and resources related to the project. It provides valuable information to help contributors and users understand the project and get involved.

## Table of Contents

- Introduction
- Getting Started
- Milton HPC
- Galaxy
- Nextflow
- Other directories


## Introduction
The core of the project is to make the HPC democratisable for [Imaging](https://imaging.wehi.edu.au/) researchers at WEHI. The project aims to propose a user friendly and easily accessible workflow for analysing 3D Lightsheet Image data using Milton HPC. It also include a detailed analysis for the platforms Galaxy and Nextflow.


For students in this project, follow these steps to get started:

1. Finish university mandatory modules for the internship placement
2. Set up WEHI workday & finish mandatory modules and courses
3. Finish [Onboarding Checklist](https://wehieduau.sharepoint.com/sites/StudentInternGroupatWEHI/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FStudentInternGroupatWEHI%2FShared%20Documents%2FImage%20Introduction%2FRDM%230138%20%5BDraft%5D%20Student%20Internship%20Onboarding%20checklist%2Epdf&parent=%2Fsites%2FStudentInternGroupatWEHI%2FShared%20Documents%2FImage%20Introduction)
4. Read [Onboarding Document](https://figshare.com/articles/online_resource/RDM_0138_RCP_Student_Onboarding_Checklist/23280815)

## Getting Started

This project work with data produced by [3D Lightsheet Microscopy](https://www.youtube.com/watch?v=afIkWHx3duc). The [presentation of previous students](https://wehieduau.sharepoint.com/:v:/r/sites/StudentInternGroupatWEHI/Shared%20Documents/Image%20Introduction/Imaging%20-%20Dingcheng%20Lu,%20Cassiel%20Huo,%20Starry%20Liu-20230525_110436-Meeting%20Recording.mp4?csf=1&web=1&e=TTs5gC) can be accessed via Teams. The [Napri Lattice Plugin](https://github.com/BioimageAnalysisCoreWEHI/napari_lattice) can serve as an example. This is an example [workflow](https://github.com/BioimageAnalysisCoreWEHI/napari_lattice/wiki/5.1-Workflows-(Custom-workflow)) and [dataset1](https://zenodo.org/record/7117784), [dataset2](https://zenodo.org/record/3362976).

## Milton HPC
Milton is the HPC used at WEHI. Follow [Milton Setup](https://wehieduau.sharepoint.com/sites/rc2/SitePages/using-milton.aspx?web=1&xsdata=MDV8MDF8fGJhMTA1Y2QwNGRiNDQ0ZTI0Mjk0MDhkYWQxYTU1OWQ4fGFhN2M3MmUyYzVjZjRhNDBhMjJhYTU4NWMwNGNhMDdjfDB8MHw2MzgwNTI4MDUzMzM1MDA1NjR8VW5rbm93bnxWR1ZoYlhOVFpXTjFjbWwwZVZObGNuWnBZMlY4ZXlKV0lqb2lNQzR3TGpBd01EQWlMQ0pRSWpvaVYybHVNeklpTENKQlRpSTZJazkwYUdWeUlpd2lWMVFpT2pFeGZRPT18MXxNVFkyT1RZNE16Y3pNalk1TXpzeE5qWTVOamd6TnpNeU5qa3pPekU1T20xbFpYUnBibWRmVGxScmVGcEhWbWhaTWtWMFRWUkdhazE1TURCTlIxbDRURlJuZWxwRVFYUk9WRVpzVFZSck1VNTZRbXhhVjFadFFIUm9jbVZoWkM1Mk1nPT18MDRhYTYxYmU5YmJiNDAxNDQyOTQwOGRhZDFhNTU5ZDh8NTExMjg2MjFiZmM0NDFiMGE2ZGUzOGQ2YWYzMDNlMmE%3D&sdata=blovM3BzRmQwV1J3YzBhRGExd2NmenpXR2VDMmxDQWVOclV3eUIzcnh5az0%3D&ovuser=0e5bf3cf-1ff4-46b7-9176-52c538c22a4d%2Csudiz%40student.unimelb.edu.au&OR=Teams-HL&CT=1670280871424&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiIyNy8yMjEwMjgwNzIwMCIsIkhhc0ZlZGVyYXRlZFVzZXIiOnRydWV9) to get started.

## Galaxy
Galaxy is an open-source, web-based platform that provides a user-friendly environment for performing data analysis, particularly in the fields of bioinformatics and computational biology. It was developed to make complex computational tools and workflows more accessible to researchers who may not have extensive programming experience.

Key features of Galaxy include: 
- Web-based Interface: Galaxy is accessible through a web browser, eliminating the need for complex installations on individual computers. This feature allows users to access the platform from anywhere with an internet connection. 
- Reproducible Workflows: Galaxy allows users to create and share workflows, which are sequences of computational steps. These workflows can be saved, shared, and reused by other researchers, ensuring the reproducibility of data analysis. 
- Tool Integration: Galaxy provides a wide range of computational tools and algorithms for various bioinformatics tasks, such as sequence analysis, genome assembly, protein structure prediction, and more. These tools are integrated into the platform and can be combined to create custom analysis workflows. 
- Data Management: Galaxy includes features for uploading, organizing, and managing data within the platform. This ensures that data used in analyses is readily available and can be easily shared with collaborators. 
- Collaboration: Galaxy allows multiple users to work on the same project simultaneously, facilitating collaboration and enabling researchers to share their analysis processes and results with others. 
- Visualization: Galaxy provides interactive visualizations and charts to help users interpret and analyze their data effectively.

### Getting Started With Galaxy
First, [Install](https://galaxyproject.org/admin/get-galaxy/) Galaxy. Follow [this tutorial](https://training.galaxyproject.org/training-material/topics/imaging/tutorials/imaging-introduction/tutorial.html) to tart using Galaxy for image analysis. Visit [Galaxy Documentation](https://docs.galaxyproject.org/en/master/#about-docs) as you need. 

Pros:
- User-Friendly Interface: Galaxy provides a web-based GUI with drag-and-drop functionality, making it accessible to researchers without programming experience.
- Extensive Toolset: Galaxy offers a wide range of pre-built tools for bioinformatics analyses, making it convenient for users to perform common tasks.
- Collaboration and Sharing: Galaxy facilitates sharing of workflows and datasets among users, promoting collaboration and enabling reproducibility.
- Managed Execution: Workflows are executed on Galaxy servers, reducing the need for users to manage computing resources.

Cons:
- Limited Flexibility: Galaxy's GUI-driven approach may be limiting for users who require more advanced customization and optimization in their workflows.
- Dependent on Galaxy's Ecosystem: Users are tied to Galaxy's toolset and may encounter limitations when using tools not available in Galaxy's environment.
- Server Resource Limitations: Public Galaxy servers may have restrictions on data storage and execution time.

## Nextflow

Nextflow is an open-source workflow management system designed to facilitate the development, execution, and sharing of data-intensive and scalable scientific workflows. It allows researchers and data scientists to define complex computational pipelines as code, making it easy to automate and reproduce their data analysis tasks across various computing environments.

Key features of Nextflow include:
- Declarative Workflow Language: Nextflow provides a domain-specific language (DSL) that allows users to define their workflows as code in a declarative manner. This DSL abstracts away the underlying computing infrastructure, making workflows portable and easily adaptable to different environments.
- Scalability and Parallel Execution: Nextflow follows a data-driven model, where tasks are executed as soon as their inputs become available. This enables parallel execution of tasks, taking full advantage of available computing resources and making it suitable for processing large-scale datasets.
- Support for Various Computing Environments: Nextflow allows workflows to be executed on diverse platforms, including local machines, high-performance computing (HPC) clusters, cloud providers (AWS, GCP, Azure), and containerized environments (Docker, Singularity). This flexibility enables seamless workflow deployment in different computational infrastructures.
- Reproducibility and Versioning: Nextflow emphasizes reproducibility by allowing users to specify software dependencies and tool versions required for each task. Workflows can be version-controlled, ensuring that results are consistent across different executions.
- Containerization Support: Nextflow integrates with container technologies like Docker and Singularity, enabling users to encapsulate software dependencies and ensure consistency across different execution environments.
- Community and Collaboration: Nextflow has a growing community of users and contributors who share their workflows and collaborate on the improvement of the platform. This collaborative aspect fosters knowledge exchange and supports the reuse of existing workflows.

### Geting Started With Nextflow
Follow the [installation](https://www.nextflow.io/docs/latest/getstarted.html#installation) to install Nextflow. Here is an [example pipeline](https://www.nextflow.io/example1.html). Refer to the [documentation](https://www.nextflow.io/docs/latest/index.html) as you need.

Pros:
- Flexibility and Portability: Nextflow allows users to define workflows as code, providing greater flexibility and portability across different computing environments.
- Scalability: Nextflow's data-driven model and parallelization capabilities enable efficient processing of large-scale data on various platforms.
- Containerization Support: Nextflow integrates with container technologies like Docker and Singularity, ensuring reproducibility across different environments.
- Versatility: Nextflow is not limited to specific scientific domains, making it suitable for various data analysis tasks beyond bioinformatics.

Cons:
- Command-Line Interface: Nextflow relies on a command-line interface, which might be less intuitive for users without programming experience.
- Initial Learning Curve: Users need to learn the Nextflow DSL and command-line commands to develop and run workflows effectively.
- Development Overhead: Creating workflows as code requires more initial development effort compared to the visual workflow design in Galaxy.
- Limited Built-in Toolset: Unlike Galaxy, Nextflow does not come with an extensive set of pre-built tools; users need to script their own tools or use third-party tools.

## Other Directories

- [Shared Drive](https://drive.google.com/drive/folders/186MxmarfeZqoJfcsiaIYojX-FTjOZioU?usp=drive_link)
- [Meeting notes](https://docs.google.com/document/d/1UEPsfUaInItshv7jPXXyo1aayWIt4zQKBGHZNqaDdr4/edit?usp=sharing)


---

Feel free to update and this wiki as you find other useful resources.
