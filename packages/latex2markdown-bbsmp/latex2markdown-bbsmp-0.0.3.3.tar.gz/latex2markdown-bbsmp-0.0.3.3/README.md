# LaTeX2Markdown

An [AMS-LaTeX][amslatex] compatible converter from (a subset of) [LaTeX][latex] to [MathJaX][mathjax] compatible [Markdown][markdown].

[amslatex]: http://en.wikipedia.org/wiki/AMS-LaTeX
[latex]: http://www.latex-project.org/
[mathjax]: http://www.mathjax.org/
[markdown]: http://daringfireball.net/projects/markdown/
[pandoc]: http://johnmacfarlane.net/pandoc/
## Who should use this?

Anyone who writes LaTeX documents using the AMS-LaTeX packages (`amsmath`, `amsthm`, `amssymb`) and wants to convert these documents to Markdown format to use with MathJaX.  These Markdown files can then be easily added to any web platform - Jekyll blogs, Wordpress, basic HTML sites, etc. 

In short, if you seek to use MathJaX to view your LaTeX documents online, then you might be interested in this.

## Demonstration

Forked from [tullo.ch/projects/LaTeX2Markdown](http://tullo.ch/projects/LaTeX2Markdown)

Check out [bbsmp/projects/LaTeX2Markdown](https://github.com/bbsmp/LaTeX2Markdown.git) for a live demonstration of the converter.


## Getting Started

### Installation

The project is available on PyPI, so getting it is as simple as using 

    pip install latex2markdown-bbsmp
    
or 

    easy_install latex2markdown-bbsmp

### Usage

The utility can be called from the command line, or from within a Python script.

For the command line, the syntax to convert a LaTeX file to a Markdown file is as follows:

    python -m latex2markdown-bbsmp path/to/latex/file path/to/output/markdown/file

For example, to compile a LaTeX file `sample.tex` into a Markdown file `sample.md`, call

    python -m latex2markdown-bbsmp sample.tex sample.md