<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />

<h3 align="center">poker</h3>
  <p align="center">
    Simple poker game with advanced AIs to play with.
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

The poker playground is a website designed to familiarize the user's understanding of poker and the some common poker AIs. Site link: 
<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Node.JS][Node.js]][Node-url]
* [![React][React.js]][React-url]
* [![MongoDB][MongoDB]][MongoDB-url]
* [![Flask][Flask]][Flask-url]
* [![Python][Python]][Python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

To run the app locally, you can either use Docker (Linux only) or separate terminals. Note that in both cases, you must contact the owners of this repositary for the MongoDB URI key.

#### Docker

https://docs.docker.com/desktop/install/linux-install/

#### Separate Terminals

* npm
  ```sh
  npm install npm@latest -g
  ```

* pip
  ```sh
  py -m ensurepip --upgrade
  ```

### Installation

#### Docker

1. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
2. Run the docker-compose file
    ```sh
    sudo docker compose up
    ```

#### Separate Terminals

1. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
2. Change into the database directory
   ```sh
   cd .\db\
   ```
3. Install NPM packages
   ```sh
   npm i
   ```
4. Start site
   ```sh
   npm run dev
   ```
5. Open a new terminal, and change into the server directory
   ```sh
   cd .\server\
   ```
6. Install Python packages
   ```sh
   pip install -e .
   ```
7. Start server
   ```sh
   python -m flask --app poker run --debug
   ```
8. Open a new terminal, and change into the site directory
   ```sh
   cd .\site\
   ```
9. Install NPM packages
   ```sh
   npm i
   ```
10. Start site
    ```sh
    npm run dev
    ```

Again, these steps will not work unless you have the MongoDB URIs.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

Open the website on [http://localhost:5173/](http://localhost:5173/), and follow the instructions on screen to play! Some refresh might be necessary to start the game.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Deploy site
- [ ] Improve CSS
- [ ] Fix bugs

See the [open issues](https://github.com/redacted24/poker/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Project Link: [https://github.com/redacted24/poker](https://github.com/redacted24/poker)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* [Poker Theory Paper](https://webdocs.cs.ualberta.ca/~jonathan/PREVIOUS/Grad/papp/thesis.html)
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/screenshot.jpg
[Node.js]: https://img.shields.io/badge/Node-D5E6CE?style=for-the-badge&logo=nodedotjs&logoColor=339933
[Node-url]: https://nodejs.org/en
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Flask]: https://img.shields.io/badge/Flask-FFFFFF?style=for-the-badge&logo=flask&logoColor=000000
[Flask-url]: https://flask.palletsprojects.com/en/3.0.x/
[MongoDB]: https://img.shields.io/badge/mongodb-00684A?style=for-the-badge&logo=mongodb&logoColor=FFFFFF
[MongoDB-url]: https://www.mongodb.com/
[Python]: https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=FFD343
[Python-url]: https://www.python.org/