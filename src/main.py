import cli
import parser_gabc_header
import parser_gabc_body
import formatter_ly_proportional

def main():
    print("Parsing arguments...")
    args = cli.parse_arguments()
    
    print("Importing gabc file...")
    gabc = cli.import_gabc_file(args.file_path)
    
    print("Splitting gabc file...")
    if "%%" in gabc:
        gabc_header = gabc.split("%%")[0]
        gabc_body = gabc.split("%%")[1]

        print("Parsing gabc header...")
        ly_metadata = parser_gabc_header.parse_gabc_header(gabc_header)
    else:
        print("No header detected.")
        gabc_body = gabc

    print("Parsing gabc body...")
    parser_gabc_body_proportional.parse_gabc_body(gabc_body)

    print("Formatting Lilypond...")
    ly_file = ly_template
    ly_file = formatter_ly_proportional.format_ly_metadata(ly_file)
    formatter_ly_proportional.format_ly_melody(ly_file)
    formatter_ly_proportional.format_ly_lyrics(ly_file)

    print("Compiling pdf...")
    cli.compile_lilypond(ly_file)


if __name__ == "__main__":
    main()
