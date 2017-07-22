from helpers import *

from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import *

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from animation.playground import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.fractals import *
from topics.number_line import *
from topics.combinatorics import *
from topics.numerals import *
from topics.three_dimensions import *
from topics.objects import *
from topics.complex_numbers import *
from topics.common_scenes import *
from topics.probability import *
from scene import Scene
from scene.reconfigurable_scene import ReconfigurableScene
from scene.zoomed_scene import *
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *

#revert_to_original_skipping_status

def get_binomial_distribution(n, p):
    return lambda k : choose(n, k)*(p**(k))*((1-p)**(n-k))

def get_quiz(*questions):
    q_mobs = VGroup(*map(TextMobject, [
        "%d. %s"%(i+1, question)
        for i, question in enumerate(questions)
    ]))
    q_mobs.arrange_submobjects(
        DOWN, 
        buff = MED_LARGE_BUFF,
        aligned_edge = LEFT, 
    )
    content = VGroup(
        TextMobject("Quiz").scale(1.5),
        Line(q_mobs.get_left(), q_mobs.get_right()),
        q_mobs
    )
    content.arrange_submobjects(DOWN, buff = MED_SMALL_BUFF)
    rect = SurroundingRectangle(content, buff = MED_LARGE_BUFF)
    rect.shift(MED_SMALL_BUFF*DOWN)
    rect.highlight(WHITE)
    quiz = VGroup(rect, content)
    quiz.scale(0.7)
    return quiz

def get_slot_group(bool_list, buff = MED_LARGE_BUFF, include_qs = True):
    lines = VGroup(*[
        Line(ORIGIN, MED_LARGE_BUFF*RIGHT)
        for x in range(3)
    ])
    lines.arrange_submobjects(RIGHT, buff = buff)
    if include_qs:
        labels = VGroup(*[
            TextMobject("Q%d"%d) for d in range(1, 4)
        ])
    else:
        labels = VGroup(*[VectorizedPoint() for d in range(3)])
    for label, line in zip(labels, lines):
        label.scale(0.7)
        label.next_to(line, DOWN, SMALL_BUFF)
    slot_group = VGroup()
    slot_group.lines = lines
    slot_group.labels = labels
    slot_group.content = VGroup()
    slot_group.digest_mobject_attrs()
    slot_group.to_edge(RIGHT)
    slot_group.bool_list = bool_list

    total_height = SPACE_HEIGHT
    base = 2.3

    for i, line in enumerate(lines):
        if i >= len(bool_list) or bool_list[i] is None:
            mob = VectorizedPoint()
        elif bool_list[i]:
            mob = TexMobject("\\checkmark")
            mob.highlight(GREEN)
            slot_group.shift(total_height*DOWN / (base**(i+1)))
        else:
            mob = TexMobject("\\times")
            mob.highlight(RED)
            slot_group.shift(total_height*UP / (base**(i+1)))
        mob.next_to(line, UP, SMALL_BUFF)
        slot_group.content.add(mob)
    return slot_group

def get_probability_of_slot_group(bool_list, conditioned_list = None):
    filler_tex = "Filler"
    if conditioned_list is None:
        result = TexMobject("P(", filler_tex, ")")
    else:
        result = TexMobject("P(", filler_tex, "|", filler_tex, ")")
    fillers = result.get_parts_by_tex(filler_tex)
    for filler, bl in zip(fillers, [bool_list, conditioned_list]):
        slot_group = get_slot_group(
            bl, buff = SMALL_BUFF, include_qs = False,
        )
        slot_group.replace(filler, dim_to_match = 0)
        slot_group.shift(0.5*SMALL_BUFF*DOWN)
        index = result.index_of_part(filler)
        result.submobjects[index] = slot_group
    return result


#########

class IndependenceOpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "Far better an ", "approximate", 
            " answer to the ", " right question",
            ", which is often vague, than an ", "exact",
            " answer to the ", "wrong question", "."
        ],
        "highlighted_quote_terms" : {
            "approximate" : GREEN,
            "right" : GREEN,
            "exact" : RED,
            "wrong" : RED,
        },
        "author" : "John Tukey",
        "quote_arg_separator" : "",
    }

class DangerInProbability(Scene):
    def construct(self):
        warning = self.get_warning_sign()
        probability = TextMobject("Probability")
        probability.scale(2)

        self.play(Write(warning, run_time = 1))
        self.play(
            warning.next_to, probability, UP, LARGE_BUFF,
            LaggedStart(FadeIn, probability)
        )
        self.dither()


    #####

    def get_warning_sign(self):
        triangle = RegularPolygon(n = 3, start_angle = np.pi/2)
        triangle.set_stroke(RED, 12)
        triangle.scale_to_fit_height(2)
        bang = TextMobject("!")
        bang.scale_to_fit_height(0.6*triangle.get_height())
        bang.move_to(interpolate(
            triangle.get_bottom(),
            triangle.get_top(),
            0.4,
        ))
        triangle.add(bang)
        return triangle

class MeaningOfIndependence(SampleSpaceScene):
    CONFIG = {
        "sample_space_config" : {
            "height" : 4,
            "width" : 4,
        }
    }
    def construct(self):
        self.add_labeled_space()
        self.align_conditionals()
        self.relabel()
        self.assume_independence()
        self.no_independence()    

    def add_labeled_space(self):
        self.add_sample_space(**self.sample_space_config)
        self.sample_space.shift(2*LEFT)
        self.sample_space.divide_horizontally(0.3)
        self.sample_space[0].divide_vertically(
            0.9, colors = [BLUE_D, GREEN_C]
        )
        self.sample_space[1].divide_vertically(
            0.5, colors = [BLUE_E, GREEN_E]
        )
        side_braces_and_labels = self.sample_space.get_side_braces_and_labels(
            ["P(A)", "P(\\overline A)"]
        )
        top_braces_and_labels, bottom_braces_and_labels = [
            part.get_subdivision_braces_and_labels(
                part.vertical_parts,
                labels = ["P(B | %s)"%s, "P(\\overline B | %s)"%s],
                direction = vect
            )
            for part, s, vect in zip(
                self.sample_space.horizontal_parts, 
                ["A", "\\overline A"], 
                [UP, DOWN],
            )
        ]
        braces_and_labels_groups = VGroup(
            side_braces_and_labels,
            top_braces_and_labels,
            bottom_braces_and_labels,
        )

        self.add(self.sample_space)
        self.play(Write(braces_and_labels_groups, run_time = 4))

    def align_conditionals(self):
        line = Line(*[
            interpolate(
                self.sample_space.get_corner(vect+LEFT),
                self.sample_space.get_corner(vect+RIGHT),
                0.7
            )
            for vect in UP, DOWN
        ])
        line.set_stroke(RED, 8)
        word = TextMobject("Independence")
        word.scale(1.5)
        word.next_to(self.sample_space, RIGHT, buff = LARGE_BUFF)
        word.highlight(RED)

        self.play(*it.chain(
            self.get_top_conditional_change_anims(0.7),
            self.get_bottom_conditional_change_anims(0.7)
        ))
        self.play(
            ShowCreation(line),
            Write(word, run_time = 1)
        )
        self.dither()

        self.independence_word = word
        self.independence_line = line

    def relabel(self):
        old_labels = self.sample_space[0].vertical_parts.labels
        ignored_braces, new_top_labels = self.sample_space[0].get_top_braces_and_labels(
            ["P(B)", "P(\\overline B)"]
        )
        equation = TexMobject(
            "P(B | A) = P(B)"
        )
        equation.scale(1.5)
        equation.move_to(self.independence_word)

        self.play(
            Transform(old_labels, new_top_labels),
            FadeOut(self.sample_space[1].vertical_parts.labels),
            FadeOut(self.sample_space[1].vertical_parts.braces),
        )
        self.play(
            self.independence_word.next_to, equation, UP, MED_LARGE_BUFF,
            Write(equation)
        )
        self.dither()

        self.equation = equation

    def assume_independence(self):
        everything = VGroup(*self.get_top_level_mobjects())
        morty = Mortimer()
        morty.scale(0.7)
        morty.to_corner(DOWN+RIGHT)
        bubble = ThoughtBubble(direction = RIGHT)
        bubble.pin_to(morty)
        bubble.set_fill(opacity = 0)

        self.play(
            FadeIn(morty),
            everything.scale, 0.5,
            everything.move_to, bubble.get_bubble_center(),
        )
        self.play(
            morty.change, "hooray", everything,
            ShowCreation(bubble)
        )
        self.dither()
        self.play(Blink(morty))
        self.dither()

        self.morty = morty

    def no_independence(self):
        for part in self.sample_space.horizontal_parts:
            part.vertical_parts.labels = None
        self.play(*it.chain(
            self.get_top_conditional_change_anims(0.9),
            self.get_bottom_conditional_change_anims(0.5),
            [
                self.independence_word.fade, 0.7,
                self.equation.fade, 0.7,
                self.morty.change, "confused", self.sample_space,
                FadeOut(self.independence_line)
            ]
        ))
        self.dither()

class IntroduceBinomial(Scene):
    CONFIG = {
        "n" : 8,
        "p" : 0.7,
    }
    def construct(self):
        self.add_title()
        self.add_bar_chart()
        self.add_p_slider()
        self.write_independence_assumption()
        self.play_with_p_value(0.2, 0.5)
        self.cross_out_assumption()
        self.play_with_p_value(0.8, 0.4)
        self.shift_weight_to_tails()


    def add_title(self):
        title = TextMobject("Binomial distribution")
        title.scale(1.3)
        title.to_edge(RIGHT)
        title.shift(2*UP)

        formula = TexMobject(
            "P(X=", "k", ")=", 
            "{n \\choose k}", 
            "p", "^k",
            "(1-", "p", ")", "^{n-", "k}",
            arg_separator = ""
        )
        formula.highlight_by_tex("k", BLUE)
        formula.highlight_by_tex("p", YELLOW)
        choose_part = formula.get_part_by_tex("choose")
        choose_part.highlight(WHITE)
        choose_part[-2].highlight(BLUE)
        formula.next_to(title, DOWN, MED_LARGE_BUFF)

        self.formula = formula
        self.title = title
        self.add(title, formula)

    def add_bar_chart(self):
        n, p = self.n, self.p
        dist = get_binomial_distribution(n, p)
        chart = BarChart(
            [dist(k) for k in range(n+1)],
            bar_names = range(n+1),
        )
        chart.to_edge(LEFT)
        self.bar_chart = chart

        self.play(LaggedStart(
            FadeIn, VGroup(*it.chain(*chart)), 
            run_time = 2
        ))

    def add_p_slider(self):
        interval = UnitInterval(color = LIGHT_GREY)
        interval.scale_to_fit_width(4)
        interval.next_to(
            VGroup(self.bar_chart.x_axis, self.bar_chart.y_axis), 
            UP, MED_LARGE_BUFF
        )
        interval.add_numbers(0, 1)
        triangle = RegularPolygon(
            n=3, start_angle = -np.pi/2,
            stroke_width = 0,
            fill_color = YELLOW,
            fill_opacity = 1,
        )
        triangle.scale_to_fit_height(0.25)
        triangle.move_to(interval.number_to_point(self.p), DOWN)
        label = TexMobject("p")
        label.next_to(triangle, UP, SMALL_BUFF)
        label.highlight(triangle.get_color())

        self.p_slider = VGroup(interval, triangle, label)
        self.play(Write(self.p_slider, run_time = 1))

    def play_with_p_value(self, *values):
        for value in values:
            self.change_p(value)
            self.dither()

    def write_independence_assumption(self):
        assumption = TextMobject("Independence assumption")
        assumption.scale(1.2)
        assumption.next_to(self.formula, DOWN, MED_LARGE_BUFF, LEFT)
        assumption.highlight(GREEN_C)

        self.play(Write(assumption, run_time = 2))
        self.dither()

        self.assumption = assumption

    def cross_out_assumption(self):
        cross = Cross(self.assumption)
        cross.highlight(GREY)
        self.bar_chart.save_state()

        self.play(ShowCreation(cross))
        self.play(self.bar_chart.fade, 0.7)
        self.dither(2)
        self.play(self.bar_chart.restore)

    def shift_weight_to_tails(self):
        chart = self.bar_chart
        chart_copy = chart.copy()
        dist = get_binomial_distribution(self.n, self.p)
        values = np.array(map(dist, range(self.n+1)))
        values += 0.1
        values /= sum(values)

        old_bars = chart.bars
        old_bars.generate_target()
        new_bars = chart_copy.bars
        for bars, vect in (old_bars.target, LEFT), (new_bars, RIGHT):
            for bar in bars:
                corner = bar.get_corner(DOWN+vect)
                bar.stretch(0.5, 0)
                bar.move_to(corner, DOWN+vect)
        old_bars.target.highlight(RED)
        old_bars.target.fade()

        self.play(
            MoveToTarget(old_bars),
            ReplacementTransform(
                old_bars.copy().set_fill(opacity = 0),
                new_bars
            )
        )
        self.play(
            chart_copy.change_bar_values, values
        )
        self.dither(2)



    #####

    def change_p(self, p):
        interval, triangle, p_label = self.p_slider
        alt_dist = get_binomial_distribution(self.n, p)
        self.play(
            ApplyMethod(
                self.bar_chart.change_bar_values,
                [alt_dist(k) for k in range(self.n+1)],
            ),
            triangle.move_to, interval.number_to_point(p), DOWN,
            MaintainPositionRelativeTo(p_label, triangle)
        )
        self.p = p

class IntroduceQuiz(PiCreatureScene):
    def construct(self):
        self.add_quiz()
        self.ask_about_probabilities()
        self.show_distribution()
        self.show_single_question_probability()

    def add_quiz(self):
        quiz = self.get_example_quiz()
        quiz.next_to(self.randy, UP+RIGHT)

        self.play(
            Write(quiz),
            self.randy.change, "pondering", quiz
        )
        self.dither()

        self.quiz = quiz

    def ask_about_probabilities(self):
        probabilities, abbreviated_probabilities = [
            VGroup(*[
                TexMobject(
                    "P(", s_tex, "=", str(score), ")", rhs
                ).highlight_by_tex_to_color_map({
                    str(score) : YELLOW,
                    "text" : GREEN,
                })
                for score in range(4)
            ])
            for s_tex, rhs in [
                ("\\text{Score}", "= \\, ???"),
                ("\\text{S}", "")
            ]
        ]
        for group in probabilities, abbreviated_probabilities:
            group.arrange_submobjects(
                DOWN, 
                buff = MED_LARGE_BUFF,
                aligned_edge = LEFT
            )
            group.to_corner(UP+LEFT)

        self.play(
            LaggedStart(FadeIn, probabilities, run_time = 3),
            self.quiz.scale_to_fit_height, 0.7*self.randy.get_height(),
            self.quiz.next_to, self.randy, RIGHT,
            self.randy.change, "confused", probabilities
        )
        self.dither()

        self.probabilities = probabilities
        self.abbreviated_probabilities = abbreviated_probabilities

    def show_distribution(self):
        dist = get_binomial_distribution(3, 0.7)
        values = map(dist, range(4))
        chart = BarChart(
            values, 
            width = 7,
            bar_names = range(4)
        )
        chart.to_edge(RIGHT)
        for short_p, bar in zip(self.abbreviated_probabilities, chart.bars):
            short_p.scale_to_fit_width(1.75*bar.get_width())
            short_p.next_to(bar, UP)

        self.play(
            LaggedStart(Write, VGroup(
                *filter(lambda m : m is not chart.bars, chart)
            )),
        )
        self.play(*[
            ReplacementTransform(
                bar.copy().stretch_to_fit_height(0).move_to(bar.get_bottom()),
                bar
            )
            for bar in chart.bars
        ])
        self.play(*[
            ReplacementTransform(p.copy(), short_p)
            for p, short_p in zip(
                self.probabilities,
                self.abbreviated_probabilities,
            )
        ])
        self.dither()

        self.bar_chart = chart

    def show_single_question_probability(self):
        prob = TexMobject(
            "P(", "\\text{Can answer a given question}", ")",
            "= 0.8"
        )
        prob.to_corner(UP+RIGHT)
        prob.highlight_by_tex("text", GREEN)
        rect = SurroundingRectangle(prob, buff = MED_SMALL_BUFF)

        self.play(
            Write(prob),
            self.randy.change, "happy", prob
        )
        self.play(ShowCreation(rect))
        self.dither()

        self.single_question_probability = VGroup(
            prob, rect
        )


    ######

    def create_pi_creature(self):
        randy = Randolph()
        randy.scale(0.7)
        randy.to_corner(DOWN+LEFT)
        self.randy = randy
        return randy

    def get_example_quiz(self):
        return get_quiz(
            "Define ``Brachistochrone'' ",
            "Define ``Tautochrone'' ",
            "Define ``Cycloid'' ",
        )

class BreakDownQuestionPatterns(IntroduceQuiz):
    def construct(self):
        self.add_parts_from_last_scene()
        self.break_down_possibilities()
        self.count_patterns()

    def add_parts_from_last_scene(self):
        self.force_skipping()
        IntroduceQuiz.construct(self)
        self.revert_to_original_skipping_status()

        chart_group = VGroup(
            self.bar_chart,
            self.abbreviated_probabilities
        )
        self.play(
            self.single_question_probability.scale, 0.8,
            self.single_question_probability.to_corner, UP+LEFT,
            chart_group.scale, 0.7, chart_group.get_top(),
            chart_group.to_edge, LEFT,
            FadeOut(self.probabilities)
        )

    def break_down_possibilities(self):
        slot_group_groups = VGroup(*[VGroup() for x in range(4)])
        bool_lists = [[]]
        while bool_lists:
            bool_list = bool_lists.pop()
            slot_group = self.get_slot_group(bool_list)
            slot_group_groups[len(bool_list)].add(slot_group)
            if len(bool_list) < 3:
                bool_lists += [
                    list(bool_list) + [True],
                    list(bool_list) + [False],
                ]

        group_group = slot_group_groups[0]
        self.revert_to_original_skipping_status()
        self.play(Write(group_group, run_time = 1))
        self.dither()
        for new_group_group in slot_group_groups[1:]:
            self.play(Transform(group_group, new_group_group))
            self.dither(2)

        self.slot_groups = slot_group_groups[-1]

    def count_patterns(self):
        brace = Brace(self.slot_groups, LEFT)
        count = TexMobject("2^3 = 8")
        count.next_to(brace, LEFT)

        self.play(
            GrowFromCenter(brace),
            Write(count)
        )
        self.dither()

    #######

    def get_slot_group(self, bool_list):
        return get_slot_group(bool_list, include_qs = len(bool_list) < 3)

class AssociatePatternsWithScores(BreakDownQuestionPatterns):
    CONFIG = {
        "score_group_scale_val" : 0.8,
    }
    def construct(self):
        self.add_slot_groups()
        self.show_score_groups()
        self.think_about_binomial_patterns()

    def add_slot_groups(self):
        self.slot_groups = VGroup(*map(
            self.get_slot_group,
            it.product(*[[True, False]]*3)
        ))
        self.add(self.slot_groups)
        self.remove(self.randy)

    def show_score_groups(self):
        score_groups = [VGroup() for x in range(4)]
        scores = VGroup()
        full_score_groups = VGroup()

        for slot_group in self.slot_groups:
            score_groups[sum(slot_group.bool_list)].add(slot_group)
        for i, score_group in enumerate(score_groups):
            score = TextMobject("Score", "=", str(i))
            score.highlight_by_tex("Score", GREEN)
            scores.add(score)
            score_group.organized = score_group.deepcopy()
            score_group.organized.arrange_submobjects(UP, buff = SMALL_BUFF)
            score_group.organized.scale(self.score_group_scale_val)
            brace = Brace(score_group.organized, LEFT)
            score.next_to(brace, LEFT)
            score.add(brace)
            full_score_groups.add(VGroup(score, score_group.organized))
        full_score_groups.arrange_submobjects(
            DOWN, buff = MED_LARGE_BUFF,
            aligned_edge = RIGHT
        )
        full_score_groups.to_edge(LEFT)

        for score, score_group in zip(scores, score_groups):
            score_group.save_state()
            self.play(score_group.next_to, score_group, LEFT, MED_LARGE_BUFF)
            self.dither()
            self.play(
                ReplacementTransform(
                    score_group.copy(), score_group.organized
                ),
                LaggedStart(FadeIn, score, run_time = 1)
            )
            self.play(score_group.restore)
        self.dither()

    def think_about_binomial_patterns(self):
        triangle = PascalsTriangle(
            nrows = 5,
            height = 3,
            width = 3,
        )
        triangle.to_edge(UP+RIGHT)
        row = VGroup(*[
            triangle.coords_to_mobs[3][k]
            for k in range(4)
        ])
        self.randy.center().to_edge(DOWN)
        bubble = ThoughtBubble()
        bubble.add_content(triangle)
        bubble.resize_to_content()
        triangle.shift(SMALL_BUFF*(3*UP + RIGHT))
        bubble.add(triangle)
        bubble.next_to(self.randy, UP+RIGHT, SMALL_BUFF)
        bubble.remove(triangle)

        self.play(
            FadeOut(self.slot_groups),
            FadeIn(self.randy),
            FadeIn(bubble)
        )
        self.play(
            self.randy.change, "pondering",
            LaggedStart(FadeIn, triangle, run_time = 4),
        )
        self.play(row.highlight, YELLOW)
        self.dither(4)

class TemptingButWrongCalculation(BreakDownQuestionPatterns):
    def construct(self):
        self.add_title()
        self.write_simple_product()

    def add_title(self):
        title = TextMobject("Tempting$\\dots$")
        title.scale(1.5)
        title.to_edge(UP)
        self.add(title)

    def write_simple_product(self):
        lhs = TexMobject("P\\big(", "Filler Blah", "\\big)", "= ")
        lhs.next_to(ORIGIN, UP+LEFT)
        p_of = lhs.get_part_by_tex("P\\big(")
        filler = lhs.get_part_by_tex("Filler")
        rp = lhs.get_part_by_tex("\\big)")
        slot_group = self.get_slot_group([True, True, False])
        slot_group.replace(filler, dim_to_match = 0)
        lhs.submobjects.remove(filler)

        rhs = VGroup(*[
            TexMobject("P(", "\\checkmark" if b else "\\times", ")")
            for b in slot_group.bool_list
        ])
        rhs.arrange_submobjects(RIGHT, SMALL_BUFF)
        rhs.next_to(lhs, RIGHT, SMALL_BUFF)
        for part, b in zip(rhs, slot_group.bool_list):
            part.highlight_by_tex_to_color_map({
                "checkmark" : GREEN,
                "times" : RED,
            })
            brace = Brace(part, UP)
            if b:
                value = TexMobject("(0.8)")
            else:
                value = TexMobject("(0.2)")
            value.highlight(part[1].get_color())
            value.next_to(brace, UP)
            part.brace = brace
            part.value = value

        question = TextMobject("What about correlations?")
        question.next_to(rhs, DOWN, LARGE_BUFF)

        self.play(
            Write(lhs),
            ShowCreation(slot_group.lines),
            LaggedStart(FadeIn, slot_group.content, run_time = 3),
            self.randy.change, "pondering"
        )
        self.dither(2)
        for part, mob in zip(rhs, slot_group.content):
            self.play(*[
                ReplacementTransform(
                    mob.copy(), subpart,
                    path_arc = np.pi/6
                )
                for subpart, mob in zip(part, [
                    p_of, mob, rp
                ])
            ])
            self.play(GrowFromCenter(part.brace))
            self.play(FadeIn(part.value))
            self.dither()
        self.dither()
        self.play(
            Write(question),
            self.randy.change, "confused"
        )
        self.dither(3)

class ThousandPossibleQuizzes(Scene):
    CONFIG = {
        "n_quiz_rows" : 25,
        "n_quiz_cols" : 40,
        "n_movers" : 100,
        # "n_quiz_rows" : 5,
        # "n_quiz_cols" : 8,
        # "n_movers" : 4,
        "quizzes_height" : 4,
    }
    def construct(self):
        self.draw_all_quizzes()
        self.show_division_by_first_question()
        self.show_uncorrelated_division_by_second()
        self.increase_second_correct_slice()
        self.second_division_among_first_wrong()
        self.show_that_second_is_still_80()
        self.emphasize_disproportionate_divide()
        self.show_third_question_results()

    def draw_all_quizzes(self):
        quizzes = self.get_thousand_quizzes()
        title = TextMobject("$1{,}000$ possible quizzes")
        title.scale(1.5)
        title.next_to(quizzes, UP)
        full_quizzes = VGroup(
            get_quiz(
                "Define ``Brachistochrone''",
                "Define ``Tautochrone''",
                "Define ``Cycloid''",
            ),
            get_quiz(
                "Define $\\dfrac{df}{dx}$",
                "Define $\\displaystyle \\lim_{h \\to 0} f(h)$",
                "Prove $\\dfrac{d(x^2)}{dx} = 2x$ ",
            ),
            get_quiz(
                "Find all primes $p$ \\\\ where $p+2$ is prime.",
                "Find all primes $p$ \\\\ where $2^{p}-1$ is prime.",
                "Solve $\\zeta(s) = 0$",
            ),
        )
        full_quizzes.arrange_submobjects(RIGHT)
        target_quizzes = VGroup(*quizzes[:len(full_quizzes)])

        self.add(full_quizzes)
        self.dither()
        self.play(
            Transform(full_quizzes, target_quizzes),
            FadeIn(title)
        )
        self.play(
            LaggedStart(
                FadeIn, quizzes, 
                run_time = 3,
                lag_ratio = 0.2,
            ),
            Animation(full_quizzes, remover = True)
        )
        self.dither()

        self.quizzes = quizzes
        self.title = title

    def show_division_by_first_question(self):
        n = int(0.8*len(self.quizzes))
        top_split = VGroup(*self.quizzes[:n])
        bottom_split = VGroup(*self.quizzes[n:])
        for split, color, vect in (top_split, GREEN, UP), (bottom_split, RED, DOWN):
            split.sort_submobjects(lambda p : p[0])
            split.generate_target()
            split.target.shift(MED_LARGE_BUFF*vect)
            for quiz in split.target:
                quiz[0].highlight(color)

        labels = VGroup()
        for num, b, split in (800, True, top_split), (200, False, bottom_split):
            label = VGroup(
                TexMobject(str(num)),
                get_slot_group([b], buff = SMALL_BUFF, include_qs = False)
            )
            label.arrange_submobjects(DOWN)
            label.next_to(split.target, LEFT, buff = LARGE_BUFF)
            labels.add(label)

        self.play(
            FadeOut(self.title),
            MoveToTarget(top_split),
            MoveToTarget(bottom_split),
        )
        for label in labels:
            self.play(FadeIn(label))
            self.dither()

        self.splits = VGroup(top_split, bottom_split)
        self.q1_split_labels = labels

    def show_uncorrelated_division_by_second(self):
        top_split = self.splits[0]
        top_label = self.q1_split_labels[0]
        n = int(0.8*len(top_split))
        left_split = VGroup(*top_split[:n])
        right_split = VGroup(*top_split[n:])
        for split, color in (left_split, GREEN_E), (right_split, RED_E):
            split.generate_target()
            for quiz in split.target:
                quiz[1].highlight(color)
        left_split.target.shift(LEFT)

        left_label = VGroup(
            TexMobject("(0.8)", "800 =", "640"),
            get_slot_group([True, True], buff = SMALL_BUFF, include_qs = False)
        )
        left_label.arrange_submobjects(RIGHT, buff = MED_LARGE_BUFF)
        left_label.next_to(left_split.target, UP)

        self.play(
            MoveToTarget(left_split),
            MaintainPositionRelativeTo(top_label, left_split),
            MoveToTarget(right_split),
        )
        self.play(FadeIn(left_label))
        self.play(LaggedStart(
            ApplyMethod, left_split,
            lambda m : (m.highlight, YELLOW),
            rate_func = there_and_back,
            lag_ratio = 0.2,
        ))
        self.dither()

        self.top_left_label = left_label
        self.top_splits = VGroup(left_split, right_split)

    def increase_second_correct_slice(self):
        left_split, right_split = self.top_splits
        left_label = self.top_left_label
        left_label_equation = left_label[0]
        movers = VGroup(*right_split[:self.n_movers])
        movers.generate_target()
        for quiz in movers.target:
            quiz[1].highlight(left_split[0][1].get_color())
        movers.target.shift(LEFT)

        new_equation = TexMobject("(0.925)", "800 =", "740")
        for i in 0, 2:
            new_equation[i].highlight(YELLOW)
        new_equation.move_to(left_label_equation)

        self.play(
            MoveToTarget(
                movers, 
                submobject_mode = "lagged_start",
                lag_factor = 4,
                run_time = 3,
            ),
            Transform(left_label_equation, new_equation)
        )
        self.dither(2)
        self.play(Indicate(left_label_equation[0]))
        self.dither()

        left_split.add(*movers)
        right_split.remove(*movers)
        self.top_left_split = left_split
        self.top_right_split = right_split
        self.top_movers = movers
        self.top_equation = left_label_equation

    def second_division_among_first_wrong(self):
        top_label, bottom_label = self.q1_split_labels
        top_split, bottom_split = self.splits
        top_left_label = self.top_left_label
        top_group = VGroup(top_split, top_left_label, top_label)

        n = int(0.8*len(bottom_split))
        left_split = VGroup(*bottom_split[:n])
        right_split = VGroup(*bottom_split[n:])
        for split, color in (left_split, GREEN_E), (right_split, RED_E):
            split.generate_target()
            for quiz in split.target:
                quiz[1].highlight(color)
        left_split.target.shift(LEFT)

        movers = VGroup(*left_split[-self.n_movers:])
        movers.generate_target()
        for quiz in movers.target:
            quiz[1].highlight(right_split.target[0][1].get_color())

        equation = TexMobject("(0.8)", "200 = ", "160")
        slot_group = get_slot_group([False, True], buff = SMALL_BUFF, include_qs = False)
        label = VGroup(equation, slot_group)
        label.arrange_submobjects(DOWN, buff = SMALL_BUFF)
        label.next_to(left_split.target, UP, SMALL_BUFF, LEFT)
        alt_equation = TexMobject("(0.3)", "200 = ", "60")
        for i in 0, 2:
            alt_equation[i].highlight(YELLOW)
        alt_equation.move_to(equation)

        self.play(top_group.to_edge, UP, SMALL_BUFF)
        self.play(
            bottom_label.shift, LEFT,
            *map(MoveToTarget, [left_split, right_split])
        )
        self.play(FadeIn(label))
        self.dither()
        self.play(
            MoveToTarget(
                movers, 
                submobject_mode = "lagged_start",
                run_time = 3,
            ),
            Transform(equation, alt_equation)
        )
        self.dither()

        left_split.remove(*movers)
        right_split.add(*movers)
        self.bottom_left_split = left_split
        self.bottom_right_split = right_split
        self.bottom_movers = movers
        self.bottom_equation = equation
        self.bottom_left_label = label

    def show_that_second_is_still_80(self):
        second_right = VGroup(
            self.bottom_left_split, self.top_left_split
        )
        second_wrong = VGroup(
            self.bottom_right_split, self.top_right_split
        )
        rects = VGroup(*[
            SurroundingRectangle(mob, buff = SMALL_BUFF)
            for mob in second_right
        ])

        num1 = self.top_equation[-1].copy()
        num2 = self.bottom_equation[-1].copy()

        equation = TexMobject("740", "+", "60", "=", "800")
        for tex in "740", "60":
            equation.highlight_by_tex(tex, YELLOW)
        slot_group = get_slot_group([True, True])
        slot_group.content[0].set_fill(BLACK, 0)
        label = VGroup(equation, slot_group)
        label.arrange_submobjects(DOWN)
        label.next_to(self.quizzes, LEFT, LARGE_BUFF)

        self.play(
            FadeOut(self.q1_split_labels),
            ShowCreation(rects)
        )
        self.play(
            FadeIn(slot_group),
            Transform(
                num1, equation[0],
                rate_func = squish_rate_func(smooth, 0, 0.7),
            ),
            Transform(
                num2, equation[2],
                rate_func = squish_rate_func(smooth, 0.3, 1),
            ),
            run_time = 2
        )
        self.play(
            Write(equation),
            *map(Animation, [num1, num2])
        )
        self.remove(num1, num2)
        self.dither()
        self.play(FadeOut(rects))

    def emphasize_disproportionate_divide(self):
        top_movers = self.top_movers
        bottom_movers = self.bottom_movers
        both_movers = VGroup(top_movers, bottom_movers)
        both_movers.save_state()

        top_movers.target = bottom_movers.copy().shift(LEFT)
        bottom_movers.target = top_movers.copy().shift(RIGHT)
        for quiz in top_movers.target:
            quiz[0].highlight(RED)
        for quiz in bottom_movers.target:
            quiz[0].highlight(GREEN)

        line = Line(UP, DOWN, color = YELLOW)
        line.scale_to_fit_height(self.quizzes.get_height())
        line.next_to(bottom_movers.target, LEFT, MED_LARGE_BUFF, UP)

        self.revert_to_original_skipping_status()
        self.play(*map(MoveToTarget, both_movers))
        self.play(ShowCreation(line))
        self.play(FadeOut(line))
        self.dither()
        self.play(both_movers.restore)
        self.dither()

    def show_third_question_results(self):
        all_splits = VGroup(
            self.top_left_split, self.top_right_split,
            self.bottom_left_split, self.bottom_right_split
        )
        proportions = [0.9, 0.8, 0.8, 0.4]
        for split, prop in zip(all_splits, proportions):
            n = int(prop*len(split))
            split.sort_submobjects(lambda p : -p[1])
            split.generate_target()
            top_part = VGroup(*split.target[:n])
            top_part.shift(MED_SMALL_BUFF*UP)
            bottom_part = VGroup(*split.target[n:])
            bottom_part.shift(MED_SMALL_BUFF*DOWN)
            for quiz in top_part:
                quiz[-1].highlight(GREEN)
            for quiz in bottom_part:
                quiz[-1].highlight(RED)

        split = self.top_left_split
        n_all_right = int(proportions[0]*len(split))
        all_right = VGroup(*split[:n_all_right])

        self.play(
            FadeOut(self.top_left_label),
            FadeOut(self.bottom_left_label),
        )
        for split in all_splits:
            self.play(MoveToTarget(split))
        self.dither()
        self.play(LaggedStart(
            ApplyMethod, all_right,
            lambda m : (m.highlight, YELLOW),
            rate_func = there_and_back,
            lag_ratio = 0.2,
            run_time = 2
        ))
        self.dither(2)

    #####

    def get_thousand_quizzes(self):
        rows = VGroup()
        for x in xrange(self.n_quiz_rows):
            quiz = VGroup(*[
                Rectangle(
                    height = SMALL_BUFF,
                    width = 0.5*SMALL_BUFF
                )
                for x in range(3)
            ])
            quiz.arrange_submobjects(RIGHT, buff = 0)
            quiz.set_stroke(width = 0)
            quiz.set_fill(LIGHT_GREY, 1)
            row = VGroup(*[quiz.copy() for y in range(self.n_quiz_cols)])
            row.arrange_submobjects(RIGHT, buff = SMALL_BUFF)
            rows.add(row)

        rows.arrange_submobjects(DOWN, buff = SMALL_BUFF)
        quizzes = VGroup(*it.chain(*rows))
        quizzes.scale_to_fit_height(self.quizzes_height)
        quizzes.to_edge(RIGHT)
        quizzes.shift(MED_LARGE_BUFF*DOWN)
        return quizzes

class AccurateProductRule(SampleSpaceScene, ThreeDScene):
    def construct(self):
        self.setup_terms()
        self.add_sample_space()
        self.dither()
        self.show_first_division()
        self.show_second_division()
        self.move_to_third_dimension()
        self.show_final_probability()
        self.show_confusion()

    def setup_terms(self):
        filler_tex = "Filler"
        lhs = TexMobject("P(", filler_tex, ")", "=")
        p1 = TexMobject("P(", filler_tex, ")")
        p2 = TexMobject("P(", filler_tex, "|", filler_tex, ")")
        p3 = TexMobject("P(", filler_tex, "|", filler_tex, ")")
        terms = VGroup(lhs, p1, p2, p3)
        terms.arrange_submobjects(RIGHT, buff = SMALL_BUFF)
        terms.to_edge(UP, buff = LARGE_BUFF)

        kwargs = {"buff" : SMALL_BUFF, "include_qs" : False}
        slot_group_lists = [
            [get_slot_group([True, True, False], **kwargs)],
            [get_slot_group([True], **kwargs)],
            [
                get_slot_group([True, True], **kwargs),
                get_slot_group([True], **kwargs),
            ],
            [
                get_slot_group([True, True, False], **kwargs),
                get_slot_group([True, True], **kwargs),
            ],
        ]
        for term, slot_group_list in zip(terms, slot_group_lists):
            parts = term.get_parts_by_tex(filler_tex)
            for part, slot_group in zip(parts, slot_group_list):
                slot_group.replace(part, dim_to_match = 0)
                term.submobjects[term.index_of_part(part)] = slot_group
        # terms[2][1].content[0].set_fill(BLACK, 0)
        # VGroup(*terms[3][1].content[:2]).set_fill(BLACK, 0)

        value_texs = ["0.8", ">0.8", "<0.2"]
        for term, tex in zip(terms[1:], value_texs):
            term.value = TexMobject(tex)
            term.value.next_to(term, UP)

        self.terms = terms
        self.add(terms[0])

    def add_sample_space(self):
        SampleSpaceScene.add_sample_space(self, height = 4, width = 5)
        self.sample_space.to_edge(DOWN)

    def show_first_division(self):
        space = self.sample_space
        space.divide_horizontally(
            [0.8], colors = [GREEN_E, RED_E]
        )
        space.horizontal_parts.fade(0.1)
        top_label = self.terms[1].copy()
        bottom_label = top_label.copy()
        slot_group = get_slot_group([False], buff = SMALL_BUFF, include_qs = False)
        slot_group.replace(bottom_label[1])
        Transform(bottom_label[1], slot_group).update(1)
        braces_and_labels = space.get_side_braces_and_labels(
            [top_label, bottom_label]
        )

        self.play(
            FadeIn(space.horizontal_parts),
            FadeIn(braces_and_labels)
        )
        self.play(ReplacementTransform(
            top_label.copy(), self.terms[1]
        ))
        self.dither()
        self.play(Write(self.terms[1].value))
        self.dither()

        space.add(braces_and_labels)
        self.top_part = space.horizontal_parts[0]

    def show_second_division(self):
        space = self.sample_space
        top_part = self.top_part
        green_red_mix = average_color(GREEN_E, RED_E)
        top_part.divide_vertically(
            [0.9], colors = [GREEN_E, green_red_mix]
        )
        label = self.terms[2].deepcopy()
        braces_and_labels = top_part.get_top_braces_and_labels(
            labels = [label]
        )

        self.play(
            FadeIn(top_part.vertical_parts),
            FadeIn(braces_and_labels)
        )
        self.play(ReplacementTransform(
            label.copy(), self.terms[2]
        ))
        self.dither()
        self.play(Write(self.terms[2].value))
        self.dither()

        space.add(braces_and_labels)
        self.top_left_part = top_part.vertical_parts[0]

    def move_to_third_dimension(self):
        space = self.sample_space
        part = self.top_left_part
        cubes = VGroup(
            Cube(fill_color = RED_E),
            Cube(fill_color = GREEN_E),
        )
        cubes.set_fill(opacity = 0)
        cubes.stretch_to_fit_width(part.get_width())
        cubes.stretch_to_fit_height(part.get_height())
        cubes[1].move_to(part, IN)
        cubes[0].stretch(0.2, 2)
        cubes[0].move_to(cubes[1].get_edge_center(OUT), IN)
        space.add(cubes)

        self.play(
            space.rotate, 0.9*np.pi/2, LEFT,
            space.rotate, np.pi/12, UP,
            space.to_corner, DOWN+RIGHT, LARGE_BUFF
        )
        space.remove(cubes)
        self.play(
            cubes[0].set_fill, None, 1,
            cubes[0].set_stroke, WHITE, 1,
            cubes[1].set_fill, None, 0.5,
            cubes[1].set_stroke, WHITE, 1,
        )
        self.dither()

        self.cubes = cubes

    def show_final_probability(self):
        cube = self.cubes[0]
        face = cube[2]
        points = face.get_anchors()
        line = Line(points[2], points[3])
        line.set_stroke(YELLOW, 8)
        brace = Brace(line, LEFT)
        label = self.terms[3].copy()
        label.next_to(brace, LEFT)

        self.play(
            GrowFromCenter(brace),
            FadeIn(label),
        )
        self.dither()
        self.play(ReplacementTransform(
            label.copy(), self.terms[3]
        ))
        self.dither()

    def show_confusion(self):
        randy = Randolph()
        randy.to_corner(DOWN+LEFT)

        self.play(FadeIn(randy))
        self.play(randy.change, "confused", self.terms)
        self.play(randy.look_at, self.cubes)
        self.play(Blink(randy))
        self.play(randy.look_at, self.terms)
        self.dither()

class ShowAllEightConditionals(Scene):
    def construct(self):
        self.show_all_conditionals()
        self.suggest_independence()

    def show_all_conditionals(self):
        equations = VGroup()
        filler_tex = "Filler"
        for bool_list in it.product(*[[True, False]]*3):
            equation = TexMobject(
                "P(", filler_tex, ")", "=",
                "P(", filler_tex, ")",
                "P(", filler_tex, "|", filler_tex, ")",
                "P(", filler_tex, "|", filler_tex, ")",
            )
            sub_bool_lists = [
                bool_list[:n] for n in 3, 1, 2, 1, 3, 2
            ]
            parts = equation.get_parts_by_tex(filler_tex)
            for part, sub_list in zip(parts, sub_bool_lists):
                slot_group = get_slot_group(
                    sub_list, 
                    buff = SMALL_BUFF,
                    include_qs = False
                )
                slot_group.replace(part, dim_to_match = 0)
                index = equation.index_of_part(part)
                equation.submobjects[index] = slot_group
            equations.add(equation)
        equations.arrange_submobjects(DOWN)

        rect = SurroundingRectangle(
            VGroup(*equations[0][7:]+equations[-1][7:]),
            buff = SMALL_BUFF
        )
        rect.shift(0.5*SMALL_BUFF*RIGHT)

        self.play(LaggedStart(
            FadeIn, equations,
            run_time = 5,
            lag_ratio = 0.3
        ))
        self.dither()
        self.play(ShowCreation(rect, run_time = 2))
        self.play(FadeOut(rect))
        self.dither()

    def suggest_independence(self):
        full_screen_rect = FullScreenFadeRectangle()
        randy = Randolph()
        randy.to_corner(DOWN+LEFT)


        self.play(
            FadeIn(full_screen_rect),
            FadeIn(randy)
        )
        self.play(PiCreatureSays(
            randy, "Let's just assume \\\\ independence.",
            target_mode = "shruggie"
        ))
        self.play(Blink(randy))
        self.dither()

class ShowIndependenceSymbolically(Scene):
    def construct(self):
        filler_tex = "Filler"
        rhs = TexMobject("=", "0.8")
        rhs.highlight_by_tex("0.8", YELLOW)
        rhs.next_to(ORIGIN, RIGHT, LARGE_BUFF)
        lhs = TexMobject("P(", filler_tex, "|", filler_tex, ")")
        lhs.next_to(rhs, LEFT)
        VGroup(lhs, rhs).scale(1.5)
        for part in lhs.get_parts_by_tex(filler_tex):
            slot_group = get_slot_group(
                [True, True, True],
                buff = SMALL_BUFF,
                include_qs = False,
            )
            slot_group.replace(part, dim_to_match = 0)
            lhs.submobjects[lhs.index_of_part(part)] = slot_group
        VGroup(*lhs[1].content[:2]).set_fill(BLACK, 0)
        condition = lhs[3]
        condition.content[2].set_fill(BLACK, 0)
        bool_lists = [
            [False], [True, False], [False, True], [True],
        ]
        arrow = Arrow(UP, DOWN)
        arrow.next_to(condition, UP)
        arrow.highlight(RED)
        words = TextMobject("Doesn't matter")
        words.highlight(RED)
        words.next_to(arrow, UP)

        self.add(rhs, lhs, arrow, words)
        self.dither()
        for bool_list in bool_lists:
            slot_group = get_slot_group(bool_list, SMALL_BUFF, False)
            slot_group.replace(condition)
            slot_group.move_to(condition, DOWN)
            self.play(Transform(condition, slot_group))
            self.dither()
            
class ComputeProbabilityOfOneWrong(Scene):
    CONFIG = {
        "score" : 2,
        "final_result_rhs_tex" : [
            "3", "(0.8)", "^2", "(0.2)", "=", "0.384",
        ],
        "default_bool" : True,
        "default_p" : "0.8",
        "default_q" : "0.2",
    }
    def construct(self):
        self.show_all_three_patterns()
        self.show_final_result()

    def show_all_three_patterns(self):
        probabilities = VGroup()
        point_8s = VGroup()
        point_2s = VGroup()
        for i in reversed(range(3)):
            bool_list = [self.default_bool]*3
            bool_list[i] = not self.default_bool
            probs = ["(%s)"%self.default_p]*3
            probs[i] = "(%s)"%self.default_q
            lhs = get_probability_of_slot_group(bool_list)
            rhs = TexMobject("=", *probs)
            rhs.highlight_by_tex("0.8", GREEN)
            rhs.highlight_by_tex("0.2", RED)
            point_8s.add(*rhs.get_parts_by_tex("0.8"))
            point_2s.add(*rhs.get_parts_by_tex("0.2"))
            rhs.next_to(lhs, RIGHT)
            probabilities.add(VGroup(lhs, rhs))
        probabilities.arrange_submobjects(DOWN, buff = LARGE_BUFF)
        probabilities.center()

        self.play(Write(probabilities[0]))
        self.dither(2)
        for i in range(2):
            self.play(ReplacementTransform(
                probabilities[i].copy(),
                probabilities[i+1]
            ))
        self.dither()
        for group in point_8s, point_2s:
            self.play(LaggedStart(
                Indicate, group,
                rate_func = there_and_back,
                lag_ratio = 0.7
            ))
            self.dither()

    def show_final_result(self):
        result = TexMobject(
            "P(", "\\text{Score} = %s"%self.score, ")", "=",
            *self.final_result_rhs_tex
        )
        result.highlight_by_tex_to_color_map({
            "0.8" : GREEN,
            "0.2" : RED,
            "Score" : YELLOW,
        })
        result[-1].highlight(YELLOW)
        result.highlight_by_tex("0.8", GREEN)
        result.highlight_by_tex("0.2", RED)
        result.to_edge(UP)

        self.play(Write(result))
        self.dither()

class ComputeProbabilityOfOneRight(ComputeProbabilityOfOneWrong):
    CONFIG = {
        "score" : 1,
        "final_result_rhs_tex" : [
            "3", "(0.8)", "(0.2)", "^2", "=", "0.096",
        ],
        "default_bool" : False,
        "default_p" : "0.2",
        "default_q" : "0.8",
    }

class ShowFullDistribution(Scene):
    def construct(self):
        self.add_scores_one_and_two()
        self.add_scores_zero_and_three()
        self.show_bar_chart()
        self.compare_to_binomial_pattern()
        self.show_alternate_values_of_p()

    def add_scores_one_and_two(self):
        scores = VGroup(
            TexMobject(
                "P(", "\\text{Score} = 0", ")",
                "=", "(0.2)", "^3",
                "=", "0.008",
            ),
            TexMobject(
                "P(", "\\text{Score} = 1", ")",
                "=", "3", "(0.8)", "(0.2)", "^2", 
                "=", "0.096",
            ),
            TexMobject(
                "P(", "\\text{Score} = 2", ")",
                "=", "3", "(0.8)", "^2", "(0.2)",
                "=", "0.384",
            ),
            TexMobject(
                "P(", "\\text{Score} = 3", ")",
                "=", "(0.8)", "^3",
                "=", "0.512",
            ),
        )
        scores.arrange_submobjects(
            DOWN, 
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )
        scores.shift(MED_LARGE_BUFF*UP)
        scores.to_edge(LEFT)
        for score in scores:
            score.highlight_by_tex_to_color_map({
                "0.8" : GREEN,
                "0.2" : RED,
            })
            score[-1].highlight(YELLOW)

        self.add(*scores[1:3])
        self.scores = scores

    def add_scores_zero_and_three(self):
        self.p_slot_groups = VGroup()

        self.dither()
        self.add_edge_score(0, UP, False)
        self.add_edge_score(3, DOWN, True)

    def add_edge_score(self, index, vect, q_bool):
        score = self.scores[index]
        prob = VGroup(*score[:3])
        brace = Brace(prob, vect)
        p_slot_group = get_probability_of_slot_group([q_bool]*3)
        p_slot_group.next_to(brace, vect)
        group = VGroup(*it.chain(p_slot_group, brace, score))

        self.play(LaggedStart(
            FadeIn, group,
            run_time = 2,
            lag_ratio = 0.7,
        ))
        self.dither(2)
        self.p_slot_groups.add(brace, p_slot_group)

    def show_bar_chart(self):
        p_terms = VGroup()
        to_fade = VGroup(self.p_slot_groups)
        value_mobs = VGroup()
        for score in self.scores:
            p_terms.add(VGroup(*score[:3]))
            to_fade.add(VGroup(*score[3:-1]))
            value_mobs.add(score[-1])
        dist = get_binomial_distribution(3, 0.8)
        values = map(dist, range(4))
        chart = BarChart(
            values, bar_names = range(4),
        )
        chart.shift(DOWN)

        new_p_terms = VGroup(*[
            TexMobject("P(", "S=%d"%k, ")")
            for k in range(4)
        ])
        for term, bar in zip(new_p_terms, chart.bars):
            term[1].highlight(YELLOW)
            term.scale_to_fit_width(1.5*bar.get_width())
            term.next_to(bar, UP)

        self.play(
            ReplacementTransform(
                value_mobs, chart.bars,
                submobject_mode = "lagged_start",
                run_time = 2
            )
        )
        self.play(
            LaggedStart(FadeIn, VGroup(*it.chain(*[
                submob 
                for submob in chart
                if submob is not chart.bars
            ]))),
            Transform(p_terms, new_p_terms),
            FadeOut(to_fade),
        )
        self.dither(2)

        chart.bar_top_labels = p_terms
        chart.add(p_terms)
        self.bar_chart = chart

    def compare_to_binomial_pattern(self):
        dist = get_binomial_distribution(3, 0.5)
        values = map(dist, range(4))
        alt_chart = BarChart(values)
        alt_chart.move_to(self.bar_chart)
        bars = alt_chart.bars
        bars.set_fill(GREY, opacity = 0.5)
        vect = 4*UP
        bars.shift(vect)
        nums = VGroup(*map(TexMobject, map(str, [1, 3, 3, 1])))
        for num, bar in zip(nums, bars):
            num.next_to(bar, UP)
        bars_copy = bars.copy()

        self.play(
            LaggedStart(FadeIn, bars),
            LaggedStart(FadeIn, nums),
        )
        self.dither(2)
        self.play(bars_copy.shift, -vect)
        self.play(ReplacementTransform(
            bars_copy, self.bar_chart.bars
        ))
        self.dither(2)
        self.play(
            VGroup(self.bar_chart, bars, nums).to_edge, LEFT
        )

        self.alt_bars = bars
        self.alt_bars_labels = nums

    def show_alternate_values_of_p(self):
        new_prob = TexMobject(
            "P(", "\\text{Correct}", ")", "=", "0.8"
        )
        new_prob.highlight_by_tex("Correct", GREEN)
        new_prob.shift(SPACE_WIDTH*RIGHT/2)
        new_prob.to_edge(UP)

        alt_ps = 0.5, 0.65, 0.25
        alt_rhss = VGroup()
        alt_charts = VGroup()
        for p in alt_ps:
            rhs = TexMobject(str(p))
            rhs.highlight(YELLOW)
            rhs.move_to(new_prob[-1])
            alt_rhss.add(rhs)

            dist = get_binomial_distribution(3, p)
            values = map(dist, range(4))
            chart = self.bar_chart.copy()
            chart.change_bar_values(values)
            for label, bar in zip(chart.bar_top_labels, chart.bars):
                label.next_to(bar, UP)
            alt_charts.add(chart)

        self.play(FadeIn(new_prob))
        self.play(Transform(new_prob[-1], alt_rhss[0]))
        point_5_probs = self.show_point_5_probs(new_prob)
        self.dither()
        self.play(Transform(self.bar_chart, alt_charts[0]))
        self.dither()
        self.play(FadeOut(point_5_probs))
        for rhs, chart in zip(alt_rhss, alt_charts)[1:]:
            self.play(Transform(new_prob[-1], rhs))
            self.play(Transform(self.bar_chart, chart))
            self.dither(2)

    def show_point_5_probs(self, mob):
        probs = VGroup()
        last = mob
        for k in range(4):
            buff = MED_LARGE_BUFF
            for indices in it.combinations(range(3), k):
                bool_list = np.array([False]*3)
                bool_list[list(indices)] = True
                prob = get_probability_of_slot_group(bool_list)
                rhs = TexMobject("= (0.5)^3")
                rhs.next_to(prob, RIGHT)
                prob.add(rhs)
                prob.scale(0.9)
                prob.next_to(last, DOWN, buff)
                probs.add(prob)
                last = prob
                buff = SMALL_BUFF

        self.play(LaggedStart(FadeIn, probs))
        self.dither()
        return probs

class ProbablyWrong(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Probably wrong!",
            run_time = 1,
        )
        self.change_student_modes(
            *["angry"]*3,
            run_time = 1
        )
        self.dither()

class ShowTrueDistribution(PiCreatureScene):
    def construct(self):
        self.remove(self.randy)
        self.add_title()
        self.show_distributions()
        self.show_emotion()
        self.imagine_score_0()

    def add_title(self):
        title = TexMobject("P(", "\\text{Correct}", ")", "=", "0.65")
        title.to_edge(UP)
        title.highlight_by_tex("Correct", GREEN)

        self.add(title)
        self.title = title

    def show_distributions(self):
        dist = get_binomial_distribution(3, 0.65)
        values = np.array(map(dist, range(4)))
        alt_values = values + [0.2, 0, 0, 0.2]
        alt_values /= sum(alt_values)
        chart = BarChart(values, bar_names = range(4))
        bars = chart.bars
        old_bars = bars.copy()
        arrows = VGroup()
        for bar, old_bar in zip(bars, old_bars):
            for mob, vect in (bar, RIGHT), (old_bar, LEFT):
                mob.generate_target()
                mob.target.do_about_point(
                    mob.get_corner(DOWN+vect),
                    mob.target.stretch, 0.5, 0
                )
            old_bar.target.highlight(average_color(RED_E, BLACK))
            old_bar.target.set_stroke(width = 0)
            arrow = Arrow(ORIGIN, UP, buff = 0, color = GREEN)
            arrow.move_to(bar.get_bottom())
            arrow.shift(3*UP)
            arrows.add(arrow)
        for arrow in arrows[1:3]:
            arrow.rotate_in_place(np.pi)
            arrow.highlight(RED)
        arrows.gradient_highlight(BLUE, YELLOW)

        self.add(chart)
        self.play(*map(MoveToTarget, it.chain(bars, old_bars)))
        self.play(
            chart.change_bar_values, alt_values,
            *map(ShowCreation, arrows)
        )
        self.dither(2)

        self.bar_chart = chart
        self.old_bars = old_bars

    def show_emotion(self):
        randy = self.randy

        self.play(FadeIn(randy))
        self.play(randy.change, "sad")
        self.play(Blink(randy))

    def imagine_score_0(self):
        prob_rect = SurroundingRectangle(self.title[-1])
        bar_rect = SurroundingRectangle(VGroup(
            self.bar_chart.bars[0], self.old_bars[0],
            self.bar_chart.bar_labels[0],
        ))

        self.play(ShowCreation(prob_rect))
        self.dither()
        self.play(ReplacementTransform(
            prob_rect, bar_rect
        ))
        self.dither()
        self.play(FadeOut(bar_rect))


    #####

    def create_pi_creature(self):
        self.randy = Randolph()
        self.randy.to_corner(DOWN+LEFT)
        return self.randy

class TeacherAssessingLiklihoodOfZero(TeacherStudentsScene):
    def construct(self):
        self.add_title()
        self.fade_other_students()
        self.show_independence_probability()
        self.teacher_reacts()

    def add_title(self):
        title = TexMobject("P(", "\\text{Correct}", ")", "=", "0.65")
        title.to_edge(UP)
        title.highlight_by_tex("Correct", GREEN)
        q_mark = TexMobject("?")
        q_mark.next_to(title[-2], UP, SMALL_BUFF)
        title.add(q_mark)

        self.add(title)
        self.title = title

    def fade_other_students(self):
        for student in self.students[0::2]:
            student.fade(0.7)
            self.pi_creatures.remove(student)

    def show_independence_probability(self):
        prob = get_probability_of_slot_group(3*[False])
        rhs = TexMobject("=", "(0.35)", "^3", "\\approx 4.3\\%")
        rhs.highlight_by_tex("0.35", RED)
        rhs.next_to(prob, RIGHT)
        prob.add(rhs)
        prob.next_to(self.teacher, UP+LEFT)
        words = TextMobject("Assuming independence")
        words.next_to(prob, UP)

        self.play(
            self.teacher.change, "raise_right_hand",
            FadeIn(words),
            Write(prob)
        )
        self.dither()

        self.ind_group = VGroup(prob, words)

    def teacher_reacts(self):
        ind_group = self.ind_group
        box = SurroundingRectangle(ind_group)
        box.set_stroke(WHITE, 0)
        ind_group.add(box)
        ind_group.generate_target()
        ind_group.target.scale(0.7)
        ind_group.target.to_corner(UP+RIGHT, MED_SMALL_BUFF)
        ind_group.target[-1].set_stroke(WHITE, 2)

        randy = self.students[1]

        self.teacher_says(
            "Highly unlikely",
            target_mode = "sassy",
            added_anims = [MoveToTarget(ind_group)],
            run_time = 2,
        )
        self.play(randy.change, "sad")
        self.dither(2)
        self.play(
            RemovePiCreatureBubble(
                self.teacher, target_mode = "guilty",
            ),
            PiCreatureSays(randy, "Wait!", target_mode = "surprised"),
            run_time = 1
        )
        self.dither(1)

class CorrelationsWith35Percent(ThousandPossibleQuizzes):
    def construct(self):
        self.add_top_calculation()
        self.show_first_split()
        self.show_second_split()
        self.show_third_split()
        self.comment_on_final_size()

    def add_top_calculation(self):
        equation = VGroup(
            get_probability_of_slot_group(3*[False]),
            TexMobject("="),
            get_probability_of_slot_group([False]),
            get_probability_of_slot_group(2*[False], [False]),
            get_probability_of_slot_group(3*[False], 2*[False]),
        )
        equation.arrange_submobjects(RIGHT, buff = SMALL_BUFF)
        equation.to_edge(UP)

        self.add(equation)
        self.equation = equation

    def show_first_split(self):
        quizzes = self.get_thousand_quizzes()
        n = int(0.65*len(quizzes))
        top_part = VGroup(*quizzes[:n])
        bottom_part = VGroup(*quizzes[n:])
        parts = [top_part, bottom_part]
        for part, color in zip(parts, [GREEN, RED]):
            part.generate_target()
            for quiz in part.target:
                quiz[0].highlight(color)
        top_part.target.shift(UP)
        brace = Brace(bottom_part, LEFT)
        prop = TexMobject("0.35")
        prop.next_to(brace, LEFT)

        term = self.equation[2]
        term_brace = Brace(term, DOWN)

        self.add(quizzes)
        self.dither()
        self.play(
            GrowFromCenter(brace), 
            FadeIn(prop),
            *map(MoveToTarget, parts)
        )
        self.dither()
        self.play(
            top_part.fade, 0.8,
            Transform(brace, term_brace),
            prop.next_to, term_brace, DOWN,
        )
        self.dither()

        self.quizzes = bottom_part
        self.quizzes.sort_submobjects(lambda p : p[0])

    def show_second_split(self):
        n = int(0.45*len(self.quizzes))
        left_part = VGroup(*self.quizzes[:n])
        right_part = VGroup(*self.quizzes[n:])
        parts = [left_part, right_part]
        for part, color in zip(parts, [GREEN, RED_E]):
            part.generate_target()
            for quiz in part.target:
                quiz[1].highlight(color)
        left_part.target.shift(LEFT)
        brace = Brace(right_part, UP)
        prop = TexMobject(">0.35")
        prop.next_to(brace, UP)

        term = self.equation[3]
        term_brace = Brace(term, DOWN)

        self.play(
            GrowFromCenter(brace),
            FadeIn(prop),
            *map(MoveToTarget, parts)
        )
        self.dither()
        self.play(
            Transform(brace, term_brace),
            prop.next_to, term_brace, DOWN
        )
        self.play(left_part.fade, 0.8)

        self.quizzes = right_part
        self.quizzes.sort_submobjects(lambda p : -p[1])

    def show_third_split(self):
        quizzes = self.quizzes
        n = int(0.22*len(quizzes))
        top_part = VGroup(*quizzes[:n])
        bottom_part = VGroup(*quizzes[n:])
        parts = [top_part, bottom_part]
        for part, color in zip(parts, [GREEN, RED_B]):
            part.generate_target()
            for quiz in part.target:
                quiz[2].highlight(color)
        top_part.target.shift(0.5*UP)
        brace = Brace(bottom_part, LEFT)
        prop = TexMobject("\\gg 0.35")
        prop.next_to(brace, LEFT)

        term = self.equation[4]
        term_brace = Brace(term, DOWN)

        self.play(
            GrowFromCenter(brace), 
            FadeIn(prop),
            *map(MoveToTarget, parts)
        )
        self.dither()
        self.play(
            Transform(brace, term_brace),
            prop.next_to, term_brace, DOWN,
        )
        self.play(top_part.fade, 0.8)
        self.dither()

        self.quizzes = bottom_part

    def comment_on_final_size(self):
        rect = SurroundingRectangle(self.quizzes)
        words = TextMobject(
            "Much more than ", "$(0.35)^3 \\approx 4.3\\%$"
        )
        words.next_to(rect, LEFT)

        self.play(
            ShowCreation(rect),
            FadeIn(words)
        )
        self.dither()































