import click
import papis.api

import logging
import http.server
import papis_zotero.server
import papis_zotero.importer


@click.group()
@click.help_option('-h', '--help')
def main():
    logger = logging.getLogger("papis:zotero")
    logger.info("library '{0}'".format(papis.api.get_lib()))


@main.command('serve')
@click.help_option('-h', '--help')
@click.option(
    "--port",
    help="Port to listen to",
    default=papis_zotero.server.zotero_port,
    type=int
)
@click.option(
    "--address",
    help="Address to bind",
    default="localhost"
)
def serve(address, port):
    """Start a zotero-connector server"""
    global logger
    server_address = (address, port)
    httpd = http.server.HTTPServer(
        server_address,
        papis_zotero.server.PapisRequestHandler
    )
    httpd.serve_forever()


@main.command('import')
@click.help_option('-h', '--help')
@click.option(
    '--from-bibtex',
    help='Import zotero library from a bibtex dump, the files fields in '
         'the bibtex files should point to valid paths',
    default=None,
    type=click.Path(exists=True)
)
@click.option(
    '--outfolder',
    help='Folder to save the imported library, if None is given the usual'
         ' papis library will be used',
    default=None
)
@click.option(
    '--link',
    help='Wether to link the pdf files or copy them',
    default=None
)
def do_importer(from_bibtex, outfolder, link):
    """Import zotero libraries into papis libraries
    """
    if from_bibtex is not None:
        papis_zotero.importer.import_from_bibtexfile(
            from_bibtex, outfolder, link
        )

if __name__ == "__main__":
    main()
