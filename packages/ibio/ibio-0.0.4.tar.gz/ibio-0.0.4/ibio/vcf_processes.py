from .bio.vcf import Vcf
import os

def vcf_peek(args):
    """Function to show first lines of a VCF file

    Input
    -----
    args : parser.parse_args()
        Dictionary with arguments given by user

    """

    filepath = os.path.abspath(args.vcf)
    lines = args.lines
    pretty = args.pretty

    vcf = Vcf(filepath)

    if all([args.head, args.tail]) is False:
        vcf.head(lines, pretty)
        vcf.tail(lines, pretty)

    if args.head:
        vcf.head(lines, pretty)

    if args.tail:
        vcf.tail(lines, pretty)
