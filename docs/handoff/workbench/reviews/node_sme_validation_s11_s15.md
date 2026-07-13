# Node → Cluster → Question map for SME validation — pilot sessions s11–s15

> **What this is.** The *previous-run* co-failure clustering across all five pilot sessions (42 communities, 174 items) resolved into proposed **nodes**, with every clustered question assigned to exactly one node. **SME task:** for each question, confirm it belongs under its node, or move it. Record verdicts in the companion CSV `node_sme_validation_s11_s15.csv` — columns `SME_verdict_(OK/MOVE/UNSURE)`, `SME_correct_node_if_MOVE`, `SME_notes`.
>
> **How to read the evidence.** Items were grouped because *the same learners fail them together* — phi correlation over learners who attempted both, robust filter N≥150 co-attempters, phi≥0.2, both-fail cell≥10. Clustering **proposes**; content **disposes**: where a behaviour community mixed skills we split it and flagged the row (⚑). Those split/seam rows deserve the closest look. `fail%` = first-attempt fail rate in the pilot (~4.5K learners).
>
> Node confidence: **B+C** = behaviour community and content family agree · **C** = content/bank only, thin behaviour. Generated 2026-07-13 from `communities.json` (previous run) + `question_details.json`.

## Coverage

| session | items | proposed nodes |
|---|---|---|
| s11 Conditional Statements | 75 | N1=15 · N2=19 · N3=25 · N4=16 |
| s12 Nested Conditional Statements | 24 | N1=8 · N2=15 · N3=1 |
| s13 Loops | 38 | N1=23 · N2=8 · N3=7 |
| s15 For Loop | 31 | N1=22 · N2=9 |
| s14 Understanding Coding Question Formats | 6 | N1=3 · N2=3 |

---
## s11 — Conditional Statements  (75 items)

### N1 · Indentation & block structure
indentation defines the block before anything runs (expected-block, unexpected-indent, legal 1/3-space, `if False:` still parses).  \
*15 items*

**cluster C1**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `7866559d-67e1-4164-8c62-82859a38a5f6` | CA_MULTIPLE_CHOICE | 36.1 | `a = 111 / b = 111 /  / if a <= b: /     print("Greater or equal") / else: / print("Not Greater")` |
| `72e4a338-a505-48a4-91db-9d04590ee560` | CA_MULTIPLE_CHOICE | 27.1 | `a = 4 / b = 3 / if a > b: /     print("Greater") / else: / print("Not Greater")` |
| `ea1bc777-00bd-469d-a696-130b766e1b28` | CA_MULTIPLE_CHOICE | 16.6 | `a = 23 / b = 999 /  / if a < b: / print("Less than")` |
| `7c1021a6-b9dc-4e27-aa63-3e756e262e2f` | CA_MULTIPLE_CHOICE | 14.4 | `a = 101 / b = 10 /  / if a != b: / print("Not Equal")` |
| `439ae0cd-ad0f-4ec1-943c-b569a9c2860a` | CA_MULTIPLE_CHOICE | 12.4 | `a = 14 / b = a * 10 /  / if b != 0: /     c = "Eureka!" /             print(c)` |
| `540d3fa7-b358-454e-aca3-d2d1343bf3d4` | CA_MULTIPLE_CHOICE | 11.4 | `a = 5 / b = 5 / if a == b: / print("Equal")` |
| `e189d1c1-f30c-40a1-8cdb-0e7cf12c45e2` | CA_MULTIPLE_CHOICE | 11.2 | `if not(False): /     print("line2") /         print("line3")` |
| `21b57840-38da-4731-8827-7174f7f91c6d` | CA_MULTIPLE_CHOICE | 9.9 | `if not(True): /     print("First Print") /         print("Second Print")` |
| `971b1c25-6901-4d3f-9ccc-8015c06f8435` | CA_MULTIPLE_CHOICE | 9.7 | `a = 7 / b = a + 5 /  / if b < 0: /     c = "Hurray!" /             print(c)` |
| `efba0fe7-5928-4490-b469-5b4398c11edb` | CA_MULTIPLE_CHOICE | 9.2 | `if 10 != 4: /    print("Yes") / else:     /    print("No")` |
| `f511e3fa-bd3e-4e47-a073-b1227d100102` | CA_MULTIPLE_CHOICE | 7.8 | `if False: /     print("line2") /         print("line3")` |

**cluster C14**  ·  ⚑ C14 split→N1 (legal 3-space indent)

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `458400aa-6a86-451e-b150-01b0a85c92dd` | CA_MULTIPLE_CHOICE | 20.6 | `if 4 != 4: /    print("Given two numbers are not equal") / else:     /    print("Given two numbers are equal")` |

**cluster C17**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `34cf7d80-323a-4bf0-b1fc-bf1905d8b78a` | CA_MULTIPLE_CHOICE | 17.3 | `if True: /     print("If Block") /         print("Inside If")` |
| `221e4ea0-e704-4163-a454-f2b20f3f71f4` | CA_MULTIPLE_CHOICE | 16.0 | `a = 55 / b = 45 /  / if a > b: / print("Greater than")` |
| `41fa5a6c-9e3d-4643-9eda-f5a6042d4278` | CA_MULTIPLE_CHOICE | 10.9 | `a = 2 / b = a*3 / if b > 0: /     c = "Yes" /         print(c)` |

### N2 · If/else execution scope & trailing statements
what runs when; unindented code after a block always runs; else pairs to nearest if.  \
*19 items*

**cluster C10**  ·  ⚑ C10 split→N2

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `781ca854-3d2f-4fed-a334-9091ad40375b` | CA_TEXTUAL | 32.9 | `a = 15 / b = 8 /  / if a > b: /     print(a - b) / print(a + b)` |

**cluster C15**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `dd29f7cf-3e77-4c7d-b506-dd02891f0491` | FIB_CODING | 76.4 | `name = input() / ______ /     print("Hello, " + name + "!") / ______ /     print("Hello, stranger!")` |
| `c93e22f4-cb7a-4bf7-bef6-a2c8a22465cf` | MULTIPLE_CHOICE | 40.8 | `STEM: In Python, while using conditional statements indentation is optional for the blocks of code.` |
| `d503a280-1034-495e-a634-97d73947b5bb` | CA_MULTIPLE_CHOICE | 35.5 | `a = "Code" / b = "Code" /  / if a == b: /     print("a and b are same") / print("a and b are different")` |

**cluster C3**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `34be084e-8252-4a23-b86a-e4a34976465d` | CA_MULTIPLE_CHOICE | 30.3 | `a = (10.12 < 20) / b = (100 != 200) /  / if a and b: /     print(not(a and b)) / else: /     print(a or b)` |
| `6567b339-4415-4392-ab2d-685543f539a6` | CA_TEXTUAL | 26.4 | `a = 11 /  / if a < 0: /     a = a * (-1) / print(a)` |
| `1435356a-c872-4e68-a71a-1beb6430549e` | CA_MULTIPLE_CHOICE | 22.9 | `a = 6 / b = 5 /  / if a < b: /     print("Less than") /     print("Inside If")` |
| `0baf266e-efbb-45ca-9402-18e98a3dd3af` | CA_TEXTUAL | 19.9 | `a = 24 / b = 10 /  / if a < b: /     print(a - b) / print(a + b)` |
| `40876e34-9e1c-48cc-a1a4-1b063f165a31` | CA_TEXTUAL | 15.8 | `a = 12 /  / if a > 0: /     a = a * (-1) /     print(a)` |
| `cfab6ee6-f550-4628-bce4-73077255b7dd` | CA_MULTIPLE_CHOICE | 5.9 | `marks = 40 / if marks > 80: /     print("A") / if marks > 65: /     print("B") / if marks > 50: /     print("C") / else: /     print("D")` |

**cluster C6**  ·  ⚑ C6 split→N2 (TWO-DEMAND: case-sensitive compare + trailing print)

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `689112ed-cf38-48e5-abd0-8fb5cdf37864` | CA_MULTIPLE_CHOICE | 18.8 | `a = "Here" / b = "HeRe" /  / if a == b: /     print("a and b are same") / print("a and b are different")` |

**cluster C7**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `36d49f0c-c7da-43b8-851e-64168769115f` | CA_TEXTUAL | 29.8 | `a = 3 /  / if a < 0: /     a = a * (-1) / print(a)` |
| `5d464970-c577-4427-972e-80bb39ea6138` | CA_TEXTUAL | 18.6 | `a = 12 / b = 6 /  / if a <= b: /     print(a - b) / print(a + b)` |
| `7ae00d90-f475-4216-a9d3-2c4a99b3f90c` | CA_MULTIPLE_CHOICE | 15.9 | `if not(not(True)): /     print("True") / else:     /     print("False")` |
| `1576f8c1-1658-4deb-a470-d32a0382a392` | CA_TEXTUAL | 10.6 | `a = 1 / b = 2 /  / if a > b: /     print(a - b) / print(a + b)` |

**cluster C9**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `ac20738e-59e7-4b71-a3ce-507b15ba164d` | CA_TEXTUAL | 48.9 | `a = 105 / b = 110 /  / if a <= b: /     print(a - b) / print(a + b)` |
| `e69fd5c6-d822-4e57-ab56-57dbb2ca8549` | CA_TEXTUAL | 42.3 | `a = 95 / b = 100 /  / if a < b: /     print(a - b) / print(a + b)` |
| `8877aa15-8b68-480d-870e-fb6a3c5b8e9d` | CA_TEXTUAL | 28.3 | `a = 3 / b = 2 /  / if a > b: /     print(a - b) / print(a + b)` |
| `7a5fc1cf-bf61-430f-a57e-ae0c0d38aed6` | CA_TEXTUAL | 26.0 | `a = 5 / b = 3 /  / if a > b: /     print(a - b) / print(a + b)` |

### N3 · Conditions as booleans
a comparison/expression evaluates to a bool that drives the branch; stored booleans `is_day=(t>=8)and(t<=15)`.  \
*25 items*

**cluster C10**  ·  ⚑ C10 seam: FIB write-the-if-header — N3(condition) / N1(syntax); registry author's call

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `5f1987a2-ee80-4bda-a093-897bff075806` | FIB_CODING | 36.0 | `age = 21 / ______: /     print("Welcome")` |
| `65a2af77-8c8b-43ac-82cf-28248b385263` | FIB_CODING | 18.6 | `a = 10 / b = 5 / ______: /     print("a is greater than b")` |

**cluster C11**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `fa5671be-0f07-48c7-88c3-0ceda0957888` | CA_TEXTUAL | 33.3 | `l = 9 / b = 9 /  / if l == b: /     print("Square") / else: /     print("Rectangle")` |
| `d7615d76-eea8-460f-aad1-7216e428ea7e` | CA_TEXTUAL | 16.3 | `age = 5 /  / is_eligible = (age >= 18) and (age <= 60) / if is_eligible: /     print("Enjoy the ride") / else: /     print("Not suggestible for the ride")` |
| `92a7488f-09fb-4a0c-b742-8ca6877a184f` | CA_TEXTUAL | 5.2 | `if 3 == 3: /     print("Equal") / else: /     print("Not Equal")` |

**cluster C12**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `d4d99ccd-128b-4ad8-8161-ad70e021f1fb` | CA_MULTIPLE_CHOICE | 16.3 | `time = 23 /  / is_day = (time >= 6) and (time <= 19) / if is_day: /     print("Have a Good Day") / else: /     print("Good Night Sweet Dreams")` |
| `8de6c582-68b2-4b30-91c5-710eaeab45f0` | CA_MULTIPLE_CHOICE | 15.1 | `a = 5 / b = 3 / if a <= b: /     print(str(a) + " is less than or equal to " + str(b)) / else: /     print(str(a) + " is greater than " + str(b))` |
| `fefc2dc0-d766-4dcf-b6b4-e70d36d5f5a0` | CA_MULTIPLE_CHOICE | 12.6 | `a = 6 / b = ((a / 2) == 0) / if b: /     print("True") / else: /     print("False")` |

**cluster C14**  ·  ⚑ C14 split→N3

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `27961bab-23ee-4b8c-80ed-f1f4fdec7a0c` | CA_TEXTUAL | 12.3 | `length = 10 / breadth = 10 /  / if length != breadth: /     print("Rectangle") / else: /     print("Square")` |
| `e5036f1d-b4db-4c30-bc66-dd5ffd8a5698` | CA_TEXTUAL | 9.2 | `if 100 == 99: /     print("Same") / else: /     print("Not same")` |

**cluster C16**  ·  ⚑ C16→N3 (trailing-space else is cosmetic; demand is eval)

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `0eba62cd-2591-4e4c-86c0-cae6a09fc6dc` | CA_MULTIPLE_CHOICE | 19.6 | `if not(False): /     print("True") / else:     /     print("False")` |
| `ecf8cd53-b41e-4d93-8519-df33b7e5ffbc` | CA_TEXTUAL | 18.1 | `l = 5 / b = 10 /  / if l == b: /     print("Square") / else: /     print("Rectangle")` |
| `b2403a5a-570c-4415-8b07-de003331005c` | CA_MULTIPLE_CHOICE | 13.6 | `a = 9999 / b = 99999 /  / if a <= b: /     print(str(a) + " is less than or equal to " + str(b)) / else:     /     print(str(a) + " is greater than " + str(b))` |

**cluster C2**  ·  ⚑ C2 split→N3 (stored booleans / ==,!= eval)

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `28a9783a-78f5-4db8-abe3-a65852dbc97b` | CA_TEXTUAL | 24.7 | `time = 5 /  / is_night = (time <= 6) or (time >= 23) / if is_night: /     print("Sleep") / else: /     print("Work")` |
| `03669b6d-3b7c-441c-990a-6a4280dacae9` | CA_TEXTUAL | 19.5 | `time = 23 /  / is_day = (time >= 8) and (time <= 15) / if is_day: /     print("Have a great Day") / else: /     print("Sweet Dreams")` |
| `8224a525-929f-4cbb-8ea0-00c783ab5e42` | CA_MULTIPLE_CHOICE | 14.0 | `a = 0 / b = 1 /  / if a <= b: /     print(str(a) + " is less than or equal to " + str(b)) / else:     /     print(str(a) + " is greater than " + str(b))` |
| `5ee2d163-60ea-4413-a6b0-e9e0697cba24` | CA_TEXTUAL | 12.4 | `length = 111 / breadth = 111 /  / if length != breadth: /     print("Rectangle") / else: /     print("Square")` |
| `7f31d394-bb51-49ad-b08c-4f3701135464` | CA_TEXTUAL | 11.8 | `length = 999 / breadth = 999 /  / if length == breadth: /     print("Square") / else: /     print("Rectangle")` |
| `e7aa2590-3d17-4359-8d08-13549ce82583` | CA_TEXTUAL | 9.3 | `if 100 == 100: /     print("Yes") / else: /     print("No")` |

**cluster C6**  ·  ⚑ C6 split→N3

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `1b9dd04a-0003-4e14-a4be-07a661f28dc8` | CA_MULTIPLE_CHOICE | 24.6 | `a = (0.5 < 1.3) / b = (3 != 3) /  / if a and b: /     print(not(a and b)) / else: /     print(a or b)` |
| `ddbd17a4-c93a-44fb-9127-2bbc025aafb0` | CA_MULTIPLE_CHOICE | 12.8 | `a = 23 / b = 20 /  / if b != a: /     print("a and b are Not Equal")` |

**cluster C8**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `49bda558-b09e-40ca-9602-071a62bd7280` | CA_MULTIPLE_CHOICE | 27.4 | `a = (2 < 5) / b = (3 != 4) / if a and b: /     print((not(a and b))) / else: /     print(a or b)` |
| `d098001b-258c-40ca-b1ea-eae4685be3b2` | CA_MULTIPLE_CHOICE | 18.1 | `a = 4 / b = 3 /  / if a == b: /     print("Equal") /     print("Inside If")` |
| `6bb5ab73-512d-4a69-9284-0393e675cbca` | CA_MULTIPLE_CHOICE | 13.9 | `if 8 != 9: /     print("Not Equal") / else: /     print("Equal")` |
| `3dc85a33-9524-418a-9fa4-134c4c3c73c7` | CA_MULTIPLE_CHOICE | 8.0 | `a = 33 / b = 200 / if b > a: /     print("b is greater than a")` |

### N4 · Sequential ifs vs ladder
independent ifs each fire; elif/else ladder is first-true-wins.  \
*16 items*

**cluster C13**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `4bf6ad4a-f436-473e-b8a3-9e1b3fa5530d` | CA_MULTIPLE_CHOICE | 15.6 | `marks = 65 /  / if marks > 85: /     print("A") / if marks > 70: /     print("B")` |
| `f8fb868e-fb97-432f-bf57-a46c44a8d73c` | CA_TEXTUAL | 7.9 | `marks = 10 /  / if marks > 85: /     print("Satisfied") / if marks > 70: /     print("Good") / if marks > 30: /     print("Average") / else: /     print("Fail")` |
| `03a83160-120b-40f3-9ad4-91df5826eebe` | CA_MULTIPLE_CHOICE | 6.9 | `marks = 12 /  / if marks > 40: /     print("A") / if marks > 35: /     print("B") / if marks > 15: /     print("C") / else: /     print("D")` |

**cluster C2**  ·  ⚑ C2 split→N4 (marks sequential-if ladder)

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `0a1d0356-36f0-4731-9343-d03bd5a54f98` | CA_MULTIPLE_CHOICE | 12.9 | `marks = 60 / if marks > 80: /     print("A") / if marks > 65: /     print("B") / if marks > 50: /     print("C") / else: /     print("D")` |
| `48706095-9ee2-4404-b102-019afbe34062` | CA_MULTIPLE_CHOICE | 9.3 | `marks = 99 /  / if marks >= 95: /     print("Satisfied") / if marks >= 80: /     print("Good") / if marks >= 40: /     print("Average") / else: /     print("Fai …` |
| `102d40c4-7125-4277-a814-62437ee67631` | CA_TEXTUAL | 7.6 | `marks = 30 /  / if marks > 90: /     print("A") / if marks > 65: /     print("B") / if marks > 50: /     print("C") / else: /     print("D")` |

**cluster C4**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `e0148f64-7e8c-4216-9512-2ace96c9b288` | CA_TEXTUAL | 21.1 | `marks = 70 /  / if marks > 85: /     print("A") / if marks > 75: /     print("B") / if marks > 50: /     print("C") / else: /     print("D")` |
| `b3a8f1da-52f7-47ab-8f40-4f208472e9dc` | CA_TEXTUAL | 16.4 | `time = 17 /  / is_day = (time >= 6) and (time <= 18) / if is_day: /     print("Day") / else: /     print("Night")` |
| `fa634c4a-812b-4a0c-93c9-26fcc9d7e4e9` | CA_TEXTUAL | 15.9 | `length = 191 / breadth = 121 /  / if length != breadth: /     print("Rectangle") / else: /     print("Square")` |
| `0a8ee992-c1d2-4e4b-b50b-c3724b48702c` | CA_MULTIPLE_CHOICE | 12.4 | `marks = 87 /  / if marks >= 90: /     print("A+") / if marks >= 75: /     print("A-") / if marks >= 50: /     print("B") / else: /     print("C")` |
| `66a90f2f-4d02-473a-88a5-635551669189` | CA_MULTIPLE_CHOICE | 8.3 | `marks = 49 /  / if marks > 70: /     print("Satisfied") / if marks > 50: /     print("Good") / if marks > 40: /     print("Average") / else: /     print("Fail")` |

**cluster C5**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `28445134-18d2-4a2a-b0e4-cc3c108d3442` | CA_TEXTUAL | 51.6 | `marks = 70 /  / if marks > 80: /     print("Brilliant") / if marks > 65: /     print("Very good") / if marks > 50: /     print("Average") / else: /     print("N …` |
| `1f748906-a0b3-4552-bb5e-1737827c12e4` | CA_TEXTUAL | 50.9 | `marks = 77 /  / if marks > 90: /     print("Excellent") / if marks > 75: /     print("Good") / if marks > 40: /     print("Average") / else: /     print("Fail")` |
| `62518ad0-6565-44f3-a1ba-f7114859b8eb` | CA_TEXTUAL | 44.5 | `marks = 89 /  / if marks > 90: /     print("A") / if marks > 75: /     print("B") / if marks > 50: /     print("C") / else: /     print("D")` |
| `8c93445a-bc1e-4a2a-8d55-9fa8f0b66f33` | CA_TEXTUAL | 38.7 | `marks = 95 /  / if marks > 80: /     print("A") / if marks > 65: /     print("B") / if marks > 50: /     print("C") / else: /     print("D")` |

**cluster C6**  ·  ⚑ C6 split→N4

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `3bd498ec-2513-43c3-8e05-589bf09a3f7a` | CA_MULTIPLE_CHOICE | 5.2 | `marks = 20 /  / if marks > 90: /     print("A+") / if marks > 65: /     print("A-") / if marks > 45: /     print("B") / else: /     print("D")` |


---
## s12 — Nested Conditional Statements  (24 items)

### N1 · Boolean-gated nesting
a stored boolean gates the outer block; the inner if is never reached when the outer is False.  \
*8 items*

**cluster C1**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `799e4cef-b061-403f-8ae3-0053083172d6` | CA_MULTIPLE_CHOICE | 68.7 | `c = (type(54/3) == type(18)) / d = ((5 ** 3) == (125)) / if c: /     print("c is True") /     if d: /         print("d is True")     / print("END")` |
| `f303b136-a260-4e14-a07c-3553ae055e3e` | CA_MULTIPLE_CHOICE | 63.6 | `condition1 = (("chillchillchill") == ("chill " * 3)) / condition2 = (( 15*3 ) > (30)) /  / sum = 24 /  / if condition1: /     sum = sum + 12 /     print(sum) /  …` |
| `97adb9d2-c37b-48e2-a263-4c1ed92963f2` | CA_MULTIPLE_CHOICE | 59.8 | `expression1 = (36 < 16) / expression2 = (True or True) / if expression1: /     print("expression1 is True") /     if expression2: /         print("expression2 i …` |
| `3e3ba06a-b0fb-44f9-a59f-699923c4aac2` | CA_MULTIPLE_CHOICE | 58.4 | `x = (True and False) / y = (False or True) / if x: /     print("x is True") /     if y: /         print("y is True")     / print("END")` |
| `e418a85a-0a15-49cb-b833-174baf4d791b` | CA_MULTIPLE_CHOICE | 52.0 | `x = ((3/4) >= (4/3)) / y = ((type(67)) == (type("67"))) /  / sum = 12 /  / if x: /     sum = sum + 54 /     print(sum) /     if y: /         sum = sum + 32 /    …` |

**cluster C2**  ·  ⚑ C2 split→N1 (boolean-gated nesting)

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `fe1cb1c6-e73f-4a4e-93ef-5a33f70dfea8` | CA_MULTIPLE_CHOICE | 21.0 | `a = (2 > 3) / b = (True and False) / if a: /     print("a is True") /     if b: /         print("b is True")     / print("END")` |
| `4161e7c1-b9d7-4b8d-b406-6bcb359fbd0a` | CA_MULTIPLE_CHOICE | 17.2 | `x = (True or False) / y = (False and True) / if x: /     print("x is True") /     if y: /         print("y is True")     / print("END")` |
| `fb292562-4c2e-4216-a44a-01c900737027` | CA_MULTIPLE_CHOICE | 17.2 | `p = (24 > 21) / q = (False or False) / if p: /     print("p is True") /     if q: /         print("q is True")     / print("END")` |

### N2 · Nested gating with comparisons/types
building the gating expression inside nests (`(36<16)`, type() equality).  \
*15 items*

**cluster C3**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `a9cb037f-c335-4939-93eb-0f47ad653bb2` | CA_MULTIPLE_CHOICE | 42.2 | `if a: /     print("I like sports") /     if b: /         print("I like Football") /     else: /         print("I like Tennis") / else: /      print("I like read …` |
| `37c47406-8267-413c-9001-caaa9039e143` | CA_MULTIPLE_CHOICE | 28.4 | `a = False / b = True /  / if a: /     if b: /         print("Both a and b are True")` |
| `7aabdbcb-046d-492e-82e9-3f9c1ec5abc1` | CA_MULTIPLE_CHOICE | 8.6 | `number = 20 / if number % 10 == 0: /     print("Divisible by 10") / elif number % 5 == 0: /     print("Divisible by 5") / else: /     print("Not Divisible by 10 …` |

**cluster C4**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `d7fe4a11-821c-4134-9a7b-e39a3dc724ec` | CA_MULTIPLE_CHOICE | 39.4 | `score = float(input()) /  / if score > 60: /     print("A") / elif (score > 40) or (score <= 60): /     print("B") / else: /     print("C")` |
| `eca0018c-5dfe-4717-ba5d-2226473e75f2` | CA_TEXTUAL | 33.5 | `a = input() / num1 = int(a[0]) / num2 = int(a[1]) / num3 = int(a[2]) / num4 = int(a[3]) /  / is_num1_smallest = ((num1 < num2) and (num1 < num3) and (num1 < num …` |
| `45972cae-cd11-4f14-9d90-74103affb32d` | CA_MULTIPLE_CHOICE | 9.7 | `a = 2 / b = 3 / c = 1 / is_a_greatest = (a > b) and (a > c) / if is_a_greatest: /     print(a) / else: /     is_b_greatest = (b > c) /     if is_b_greatest: /   …` |

**cluster C5**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `239a1da6-f476-4f46-a2af-7367077a99b9` | CA_MULTIPLE_CHOICE | 16.4 | `grade = float(input()) /  / if grade > 95: /     print("Very Good") / elif grade > 65: /     print("Good") / else: /     print("Better Luck Next Time!")` |
| `823719c2-657e-4d48-986b-adf27c70e4a7` | CA_MULTIPLE_CHOICE | 9.9 | `grade = float(input()) /  / if grade > 90: /     print("A") / elif (grade > 70) and (grade <= 90): /     print("B") / else: /     print("C")` |
| `5bd5e9e3-bed7-4a43-9ee5-d54b73dd48ef` | CA_MULTIPLE_CHOICE | 8.9 | `points = float(input()) /  / if points > 80: /     print("Very Good") / elif points > 60: /     print("Good") / else: /     print("Better Luck Next Time!")` |

**cluster C6**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `2d34fbeb-acd0-427f-9b99-3773ea98e793` | CA_TEXTUAL | 37.3 | `a = input() / num1 = int(a[0]) / num2 = int(a[1]) / num3 = int(a[2]) / num4 = int(a[3]) /  / is_num1_smallest = ((num1 < num2) and (num1 < num3) and (num1 < num …` |
| `5158f651-0e97-40fa-9fd1-7068b280137d` | CA_MULTIPLE_CHOICE | 22.1 | `number = 20 / if number % 10 == 0: /     print("Divisible by 10") / elif: /     print("Divisible by 5") / else: /     print("Divisible by 5")` |
| `9f26c8a0-7b23-4ab5-ae9e-cf8ba9ab7237` | MULTIPLE_CHOICE | 22.1 | `STEM: Why is indentation crucial when writing nested conditional statements in Python?` |

**cluster C7**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `7bacc79f-ec67-402e-9419-28e3bc02dee5` | CA_MULTIPLE_CHOICE | 60.3 | `word_1 = "Microwave" / word_2 = "Wavelength"  / expression1 = (word_1[5:9] == word_2[:4]) / expression2 = (333 == ("3" * 3)) / if expression1: /     print("expr …` |
| `cbb04b93-b009-4e74-8a78-a879352c1e3e` | CA_MULTIPLE_CHOICE | 19.8 | `a = 2 / b = 3 / c = 1 / is_a_greatest = (a > b) and (a > c) / if is_a_greatest: /     print(a) / else: /     is_b_greatest = (b > c) /     if is_b_greatest: /   …` |
| `99072b33-db0a-43b6-bba0-99ae28a648b6` | CA_MULTIPLE_CHOICE | 16.1 | `score = float(input()) /  / if score > 90: /     print("Very Good") / elif score > 80: /     print("Good") / else: /     print("Better Luck Next Time!")` |

### N3 · elif ladder semantics
first-true-wins; both-false prints nothing; elif-after-else illegal.  \
*1 items*

**cluster C2**  ·  ⚑ C2 split→N3 (elif ladder, both-false→no output)

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `6445782f-049b-4210-9267-f3d1396f58e6` | CA_MULTIPLE_CHOICE | 22.9 | `a = False / b = False /  / if a: /     print("a is True") / elif b: /     print("b is True")` |


---
## s13 — Loops  (38 items)

### N1 · While trace & accumulation
simulate counter/accumulator to the end (sums, factorial, both-ends-moving, filtered counts).  \
*23 items*

**cluster C1**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `b0d2e2b9-aa3a-47e7-8a58-f8cfb04064e2` | CA_MULTIPLE_CHOICE | 46.0 | `a = 12 / count = 0 / while a > 0: /     a = a - 1 /     if (a < 3) or (a > 9): /         count = (count + 1) / print(count)` |
| `37b29df6-faf1-4509-aae9-2450ba8ed46f` | CA_TEXTUAL | 44.3 | `m = 20 / sum = 0 / while m <= 30: /     if (m % 2) == 0: /         sum = (sum + 1) /     if (m % 5) == 0: /         sum = (sum + 2) /     m = (m + 1) /      / p …` |
| `86aa6a16-191e-4682-a875-9aff9da31f81` | CA_TEXTUAL | 38.0 | `number = 4 / fact = 1 / while number > 0: /     fact = (fact * number) /     number = (number - 1) /  / print(fact)` |
| `6c4bc229-ed80-4082-9713-8dfa6eae1f1d` | CA_TEXTUAL | 37.9 | `a = 1 / b = 5 / counter = 0 / sum = 0 / while counter < 4: /     sum = (sum + a + b) /     a = (a + 1) /     b = (b + 1) /     counter = counter + 1 /  / print( …` |
| `b8b6e171-bb7b-4e12-be28-87a381b96d80` | CA_MULTIPLE_CHOICE | 31.0 | `a = 5 / count = 0 / while a > 0: /     a = (a - 1) /     count = (count + a) /  / print(count)` |

**cluster C11**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `ef17f8d5-b61e-477b-b020-b305087fe1e2` | CA_TEXTUAL | 53.2 | `a = 6 / i = 0 / while i <= a: /     if (i % 2) == 0: /         print(i * i) /     i = (i + 1)` |
| `6a1424dc-6eb2-4c57-8b04-74a900f19589` | CA_TEXTUAL | 34.8 | `n = 1 / while n < 5: /     print(n % 2) /     n = (n + 1)` |
| `ca1dd7ec-3b24-4a68-be6c-4b25e4f8797c` | CA_MULTIPLE_CHOICE | 23.3 | `a = 18 / i = 1 / count = 0 / while i <= a: /     if (i % 2) == 1: /         count = (count + 1) /     i = (i + 1) / print(count)` |

**cluster C2**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `e158cb7a-3341-4e51-a746-362726385798` | CA_TEXTUAL | 48.1 | `m = 1 / sum = 1 / while m <= 20: /     if (m % 2) == 0: /         sum = (sum + 1) /     if (m % 5) == 0: /         sum = (sum + 2) /     m = (m + 1) /      / pr …` |
| `8d3e7424-6715-4529-b4a1-b4eeaf765d86` | CA_TEXTUAL | 45.0 | `m = 15 / sum = 0 / while m <= 30: /     if (m % 2) == 0: /         sum = (sum + 1) /     if (m % 5) == 0: /         sum = (sum + 2) /     m = (m + 1) /      / p …` |
| `5d4183d9-2988-4bac-93da-2578471c0b3c` | CA_TEXTUAL | 38.5 | `a = 5 / c = 1 / sum = 0 / while c < a: /     sum = ((sum + a) + c) /     a = (a - 1) /     c = (c + 1) / print(sum)` |
| `6b70bc65-004c-4a95-9a46-0ccd9f8c6355` | CA_TEXTUAL | 35.2 | `a = 3 / b = 4 / counter = 1 / sum = 0 / while counter < 4: /     sum = (sum + a + b) /     a = (a + 1) /     b = (b + 1) /     counter = counter + 1 /  / print( …` |
| `6b921502-9f18-4025-9767-f0ad6b2ba689` | CA_TEXTUAL | 23.7 | `a = 5 / count = 1 / while (a > 2) and (a < 5): /     if (a % 2) == 0: /         count = (count + 2) /         a = (a + 2) /     else: /         count = (count - …` |

**cluster C3**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `39ec96a0-12db-4223-8231-2d5c79bb9065` | CA_TEXTUAL | 42.5 | `word = "Python" / counter = 2 / length_of_the_word = len(word) /  / while counter < length_of_the_word: /     print(word[counter]) /     counter = (counter + 1)` |
| `e12be295-ecbf-45e5-bd9e-abb1e1072eb6` | CA_TEXTUAL | 40.3 | `number = 5 / fact = 1 / while number > 0: /     fact = (fact * number) /     number = (number - 1) /  / print(fact)` |
| `cc7799fa-7f6f-4f9c-b099-06ce1adc8aa9` | CA_TEXTUAL | 38.8 | `a = 8 / c = 1 / sum = 0 / while c < a: /     sum = ((sum + a) + c) /     a = (a - 1) /     c = (c + 1) / print(sum)` |
| `4acf7edc-6d8e-4077-82d4-fd270049f135` | CA_MULTIPLE_CHOICE | 31.6 | `a = 8 / count = 0 / while a > 0: /     a = (a - 1) /     count = (count + a) /  / print(count)` |

**cluster C4**  ·  ⚑ C4 split→N1

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `03e89465-14fc-47ca-ba0e-02c91a8d93d2` | CA_TEXTUAL | 37.2 | `number = 3 / fact = 1 / while number > 0: /     fact = (fact * number) /     number = (number - 1) /  / print(fact)` |
| `f0043edd-0b65-44d7-a07f-6b949ce291a0` | CA_TEXTUAL | 32.6 | `n = 3 / while n < 9: /     print(n % 2) /     n = (n + 1)` |

**cluster C6**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `76a6b938-91b3-440d-9037-c89571d58839` | CA_TEXTUAL | 41.2 | `a = 8 / c = 2 / sum = 0 / while c < a: /     sum = ((sum + a) + c) /     a = (a - 1) /     c = (c + 1) / print(sum)` |
| `55fb9a8e-c989-45b7-8cc2-05759923232a` | CA_MULTIPLE_CHOICE | 37.3 | `a = True / while a: /     print("Work") /     a = True / print("Ends")` |
| `49d2bbaf-8045-408a-ba57-09a3f9054df1` | CA_MULTIPLE_CHOICE | 15.4 | `a = 17 / i = 2 / count = 0 / while i <= a: /     if (i % 2) == 0: /         count = (count + i) /     i = (i + 1) / print(count)` |

**cluster C7**  ·  ⚑ C7 split→N1 (trace `print(n%2)`)

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `e6f78e79-1794-447e-836b-cc088d721eca` | CA_TEXTUAL | 35.0 | `n = 1 / while n < 3: /     print(n % 2) /     n = (n + 1)` |

### N2 · Loop state & termination semantics
missing update→infinite; entry-condition-false→never runs; captured condition; runs-once; loop syntax/vocabulary.  \
*8 items*

**cluster C7**  ·  ⚑ C7 split→N2 (loop syntax / vocabulary — definitional)

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `18da9692-5b1d-4a39-8cfb-f908d71c99ce` | MULTIPLE_CHOICE | 18.8 | `STEM: Below code snippet is the correct syntax for a while loop in Python.

```text
while condition: 
    code block
```` |
| `9e9e63de-cd70-428a-92a3-e987a51f03c1` | MULTIPLE_CHOICE | 14.7 | `STEM: In programming, ______ is used to execute a block of code several times as long as the condition is True.` |

**cluster C8**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `7f1940ee-34ab-43fe-afa6-5ff492a1879f` | CA_MULTIPLE_CHOICE | 47.6 | `i = 0 / while i < 5: /     print(i) /     i = i + 1` |
| `21ddb473-83ec-402f-8d49-c390417511e3` | CA_MULTIPLE_CHOICE | 27.3 | `counter = 0 / while counter < 3: /     print("Python is fun!")` |
| `4c85f075-9093-45c9-90ef-e702290889ed` | CA_MULTIPLE_CHOICE | 24.6 | `a = 6 / counter = 4 / condition = (counter < 2) / while condition: /     a = a + 1 /     print(a) /     counter = counter + 1` |

**cluster C9**  ·  ⚑ C9→N2 (all entry-condition-false → never runs)

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `8cf0f56c-c7b8-4d91-861a-6b5349f45f1e` | CA_MULTIPLE_CHOICE | 26.7 | `a = 0 / counter = 1 / count = 0 / while counter <= a: /     count = (count + 1) /     counter = (counter + 1) /  / print(count)` |
| `aaa1ab04-9da6-4399-923c-5eab80efc9f4` | CA_MULTIPLE_CHOICE | 20.1 | `a = 4 / counter = 3 / while counter < 1: /     a = a + 1 /     print(a) /     counter = (counter + 1) / print("End")` |
| `ffb73136-11cd-436b-a804-fc112e7e6598` | CA_MULTIPLE_CHOICE | 16.6 | `a = 0 / while a > 0: /     print(a + 1) /     a = a - 1` |

### N3 · Boundary & filtered accumulation
`<` vs `<=`, `%` filters inside the loop, zero-iteration edges.  \
*7 items*

**cluster C10**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `f7b59138-bac5-4c07-aa3c-3967a608f063` | CA_TEXTUAL | 45.2 | `a = 10 / i = 1 / while i <= a: /     if (i % 2) == 0: /         print(i * i) /     i = (i + 1)` |
| `6b87081b-7ae4-4260-86f7-0ee2781b7a5f` | CA_MULTIPLE_CHOICE | 43.9 | `n = 4 / row = 0 / while row < n: /     print("* " * n) /     row = row` |
| `f7cf0eaa-ede7-4189-a8ce-1423ed07a2fb` | CA_TEXTUAL | 18.5 | `a = 3 / b = 6 / counter = 0 / sum = 0 / while counter < 0: /     sum = (sum + a + b) /     a = (a + 1) /     b = (b + 1) /     counter = counter + 1 /  / print( …` |

**cluster C4**  ·  ⚑ C4 split→N3 (`while i<=a` + `%2` filtered sum)

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `bfa71718-243b-4a7b-b08f-b585078f498e` | CA_MULTIPLE_CHOICE | 23.9 | `a = 10 / i = 1 / count = 0 / while i <= a: /     if (i % 2) == 0: /         count = (count + i) /     i = (i + 1) / print(count)` |

**cluster C5**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `8ce95b05-028f-4aa2-8685-6401340b9202` | CA_TEXTUAL | 44.6 | `a = 4 / i = 1 / while i <= a: /     if (i % 2) == 0: /         print(i * i) /     i = (i + 1)` |
| `51af25e8-3a4f-4f75-b6d3-7c63960df499` | CA_TEXTUAL | 30.9 | `n = 9 / while n < 15: /     print(n % 2) /     n = (n + 1)` |
| `324bc659-3b60-451c-b2b7-9966ae7e1f77` | CA_MULTIPLE_CHOICE | 24.3 | `a = -1 / count = 0 / while a > 0: /     a = (a - 1) /     count = (count + a) /  / print(count)` |


---
## s15 — For Loop  (31 items)

### N1 · range()/for trace & accumulation
range bounds & zero-iteration, accumulate/factorial, `range` evaluated once, `%`-filtered sums (the session's core skill).  \
*22 items*

**cluster C1**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `b79c7d65-4931-432f-af92-9ba17d4da31f` | CA_TEXTUAL | 58.8 | `sentence = "It's a thriller movie" / character = "l" / count = 2 /  / for each_char in sentence: /     if each_char == character: /         count = count + 1 /  …` |
| `8b7c98e2-b81a-46d0-803c-21461fd785dd` | CA_TEXTUAL | 46.7 | `count = 0 /  / for i in range(1, 10): /     count = count + 1 /      / print(count)` |
| `864f8177-9ffa-4f39-a0c6-36df81d502b7` | CA_TEXTUAL | 46.1 | `fact = 5 /  / for i in range(1, 5): /     fact = (fact * i) /      / print(fact)` |
| `d6eed841-a0da-41c0-8afd-735042426613` | CA_TEXTUAL | 45.4 | `digit = 1 / total = 99 /  / for i in range(1, digit): /     total = (total + 2) /      / print(total)` |
| `c70306c4-8a2a-48ad-bc0d-4a8b8c1cb837` | CA_TEXTUAL | 45.2 | `fact = 10 /  / for i in range(1, 6): /     fact = (fact * i) /      / print(fact)` |
| `fcf28486-e922-4264-9b80-f0d13c730dc2` | CA_MULTIPLE_CHOICE | 43.2 | `fact = 100 /  / for i in range(4): /     fact = (fact * i) /      / print(fact)` |
| `2085e437-f0f8-43b3-99f3-f2bf003e680a` | CA_MULTIPLE_CHOICE | 40.7 | `sentance = "Welcome to CCBP" / length_of_sentance = len(sentance) /  / for i in range(length_of_sentance): /     if sentance[i] == " ": /         print(sentance …` |
| `aa5370af-f53c-4538-b3b5-9ee95b8b9a04` | CA_TEXTUAL | 40.7 | `fact = 1 /  / for i in range(1, 4): /     fact = (fact * i) /      / print(fact)` |
| `e4284873-7903-45a3-a3a4-a21aaf5f4714` | CA_MULTIPLE_CHOICE | 40.5 | `number = 20 /  / for i in range(number): /     number = (number - 1) /  / print(number)` |
| `af480cdd-56e0-48ab-aa07-bdb98cef1e62` | CA_TEXTUAL | 39.7 | `starting_num = 10 / ending_num = 20 / total = 0 /  / for i in range(starting_num, ending_num): /     if (i % 5) == 0: /         total = total + i /          / p …` |
| `96f923b2-243f-4f96-9b24-4a142d9353aa` | CA_TEXTUAL | 39.3 | `number1 = 1 / number2 = 15 / total = 0 /  / for i in range(number1, number2): /     if (i % 3) == 0: /         total = total + i /          / print(total)` |
| `74c86050-90c5-4323-a4e4-3c088b40555a` | CA_TEXTUAL | 36.5 | `result = 10 /  / for i in range(1, 5): /     result = result - 1 /      / print(result)` |
| `b9dd9ea2-b6e1-48c7-a508-e8c091443ba3` | CA_TEXTUAL | 36.1 | `book = "Physics World" / character = "s" / count = 0 /  / for each_char in book: /     if each_char == character: /         count = count + 1 /          / print …` |
| `ddfe276f-0125-48bb-b4a0-c3f25cdd967d` | CA_TEXTUAL | 35.3 | `count = 100 /  / for i in range(1, 12): /     count = count - 1 /      / print(count)` |
| `8d90295d-f753-4622-ad02-654f875d8330` | CA_TEXTUAL | 34.5 | `start = 3 / end = 10 / total = 0 /  / for i in range(start, end): /     if (i % 2) == 0: /         total = total + i /          / print(total)` |
| `48d2954b-0ef5-41d6-b0f3-96bbf5ba5412` | CA_TEXTUAL | 34.4 | `number = 5 / count = 100 /  / for i in range(1, number): /     count = (count - 2) /      / print(count)` |
| `79bf495c-51f4-4dc9-9c0e-d027a87805e6` | CA_TEXTUAL | 34.1 | `first_num = 15 / last_num = 30 / total = 0 /  / for i in range(first_num, last_num): /     if (i % 4) == 0: /         total = total + i /          / print(total …` |
| `45057810-7f24-4a27-a984-f48cfc59efa0` | CA_MULTIPLE_CHOICE | 21.6 | `number = 10 / total = 80 /  / for i in range(1, number): /     if (i % 3) == 0: /         total = (total + i) /          / print(total)` |
| `1c243d15-f0b9-45ad-a7fe-7aa46b834b91` | CA_MULTIPLE_CHOICE | 19.3 | `number = 15 / total = 90 /  / for i in range(1, number): /     if (i % 4) == 2: /         total = (total + i) /  / print(total)` |

**cluster C4**  ·  ⚑ C4 split→N1 (range eval-once / factorial*0)

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `6805d328-e1bc-493d-b2cd-5afeb8c55f91` | CA_MULTIPLE_CHOICE | 49.4 | `x = 2 / for i in range(x): /     x = (x + 1) /     print (x)` |
| `e878f4c6-8bf4-44a3-94fb-44a612171915` | CA_MULTIPLE_CHOICE | 30.7 | `fact = 5 /  / for i in range(4): /     fact = (fact * i) /      / print(fact)` |

**cluster C5**  ·  ⚑ C5 split→N1 (`range(1,n)` accumulate)

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `3d431459-eb2a-41a2-9857-55a3a8fc45f4` | CA_TEXTUAL | 37.0 | `number = 10 / total = 100 /  / for i in range(1, number): /     total = (total - 2) /      / print(total)` |

### N2 · Iterating strings/slices
`for ch in s`, `for ch in s[:k]`, `for d in str(n)`, index scans.  \
*9 items*

**cluster C2**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `0e4eb770-94a1-48a7-be1f-d07f26b9c729` | CA_MULTIPLE_CHOICE | 21.0 | `book = "Alchemist" / part = "" /  / for i in book[6:]: /     part = part + i /  / print(part)` |
| `b371b85c-0d24-4912-9c56-421a4989854c` | CA_MULTIPLE_CHOICE | 20.5 | `country = "America" / part = "" /  / for i in country[4:]: /     part = part + i /  / print(part)` |
| `0217e37b-9914-407a-a3d6-6f81d647048b` | CA_MULTIPLE_CHOICE | 16.7 | `subject = "Zoology" / part = "" /  / for i in subject[3:]: /     part = part + i /  / print(part)` |

**cluster C3**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `385afe41-fb84-4d36-9ffb-f9b335c1289d` | CA_MULTIPLE_CHOICE | 45.2 | `phrase = "Buttery Popcorn" / length_of_phrase = len(phrase) /  / for i in range(length_of_phrase): /     if phrase[i] == " ": /         print(phrase[:i])` |
| `4a779232-3121-4896-aae8-94e3d4655583` | CA_MULTIPLE_CHOICE | 44.0 | `number = 10 / for digit in str(number): /     print(digit)` |
| `91753a74-5ac9-4e6e-8073-9372525d5cb2` | CA_MULTIPLE_CHOICE | 25.7 | `plant = "Aloe Vera" /  / for digit in str(plant): /     print(digit)` |

**cluster C4**  ·  ⚑ C4 split→N2 (string scan for space)

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `2956637e-858a-4224-8171-10b717919649` | CA_MULTIPLE_CHOICE | 42.2 | `word = "Home Work" / length_of_the_word = len(word) / for i in range(length_of_the_word): /     if word[i] == " ": /         print(word[:i])` |

**cluster C5**  ·  ⚑ C5 split→N2 (slice `word[:k]` build)

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `9d7db3ce-3de1-474b-9dff-ad4fee0bfd05` | CA_TEXTUAL | 37.4 | `word = "Programming" / new_word = "" /  / for each_char in word[:3]: /     new_word = (new_word + each_char) /  / print(new_word)` |
| `f991397e-4724-44aa-9bf0-11a552f5ff38` | CA_TEXTUAL | 26.5 | `greeting = "Hello World" / new_word = "" /  / for each_char in greeting[:5]: /     new_word = (new_word + each_char) /  / print(new_word)` |


---
## s14 — Understanding Coding Question Formats  (6 items)

### N1 · Problem-statement translation
read a story problem and pick its technical form.  \
*3 items*

**cluster C1**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `f65df76a-b2df-41f0-b7cb-4507019cabf3` | MULTIPLE_CHOICE | 19.5 | `STEM: Which of the following options is the correct form of the technical format of the given story-based question text?  

**Story-Based Question Text:**  
Ben …` |
| `f43465d6-e132-4f74-97f3-f94dc0a25da7` | MULTIPLE_CHOICE | 15.3 | `STEM: Which of the following options is the correct form of the technical format of the given story-based question text?  

**Story-Based Question Text:**  
Lin …` |
| `f01c350e-0089-401b-bee7-1fb9bcda5256` | MULTIPLE_CHOICE | 10.9 | `STEM: Which of the following options is the correct form of the technical format of the given story-based question text?  

**Story-Based Question Text:**  
Sar …` |

### N2 · Plan-level sequencing
order the pseudo-code / solution steps (REARRANGE).  \
*3 items*

**cluster C2**

| question_id | type | fail% | code / stem |
|---|---|---|---|
| `5b83c111-4f41-4fc1-895d-5c86b05acfd5` | REARRANGE | 24.6 | `STEM: Liam wants to write a program that counts the occurrences of a specific element in a list. Convert the given code into pseudo code.  

**Code:**

```pytho …` |
| `e8b0fbc2-9a8b-4b0a-ad73-047e067f25d4` | REARRANGE | 11.8 | `STEM: Michael wants to create a function that calculates the sum of all numbers in a list. Rearrange the options to convert the provided code into pseudo code.  …` |
| `d49f74d6-1fa6-4a35-b5ad-0df8e73269d8` | REARRANGE | 8.5 | `STEM: Anna is learning coding by going through different codes. Rearrange the given options in the correct order according to the given code snippet to help her …` |

