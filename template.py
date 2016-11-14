import re
import os
from clipboard import PyClipboard


class TemplateGenerator():

    def __init__(self, template, output):
        self.template = template
        self.output = output
        self.score_pattern = re.compile("\/([0-9]*)]")
        self.template_pattern = re.compile("\{([A-z]*[0-9]*)\}")

    def _get_score_in_line(self, text):
        result = 0
        for match in self.score_pattern.finditer(text):
            result += sum([int(x) for x in match.groups()])
        return result

    def interactive_template(self):
        """Go through each category and interactively input feedback"""
        result = ""
        score_total = 0
        score_received = 0
        with open(self.template, "r") as f:
            for line in f:
                print(line)
                if (self.template_pattern.search(line)):
                    score_total += self._get_score_in_line(line)
                else:
                    # Blindly append all the non-templated lines to the output.
                    result += line

                for match in self.template_pattern.finditer(line):
                    default_score = int(match.group(1))
                    score = input("Mark:\n>")

                    if (score.isdigit()):
                        score = int(score)
                    # Subtract the input from total if it starts with -
                    elif (score and score[0] == '-' and score[1::].isdigit()):
                        score = default_score - int(score[1::])
                    else:
                        score = default_score

                    score_received += score
                    additional_notes = input("Notes:\n>") + "\n\n"
                    result += line.replace(match.group(), str(score))
                    result += additional_notes

        result += "Total: [{0}/{1}]".format(score_received, score_total)
        return result

    def loop(self):
        running = True

        with PyClipboard() as clipboard:
            while(running):
                # call cls on windows, clear on unix
                os.system('cls' if os.name == 'nt' else 'clear')
                result = self.interactive_template()
                clipboard.clear_clipboard()
                clipboard.copy_to_clipboard(result)
                with open(self.output, "w") as f:
                    f.write(result)
                user_input = input("Continue? (Y/N)\n>")
                running = user_input[0].lower() == 'y' if user_input else False

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="\
    Interactively generate feedback from a template file")

    parser.add_argument("input", type=str, nargs="?",
                        default="template.txt")

    parser.add_argument("output", type=str, nargs="?",
                        default="out.txt")
    args = parser.parse_args()

    generator = TemplateGenerator(args.input, args.output)
    generator.loop()
