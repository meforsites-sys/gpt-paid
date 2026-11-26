/* الامتحان الوزاري المحاكي — الدور الأول 2027 | بيانات */
window.EXAM_DATA = {
  title: 'امتحان وزاري محاكي',
  round: 'الدور الأول 2027',
  subject: 'اللغة الإنجليزية — الصف السادس الإعدادي',
  durationMin: 150,
  note: 'في الورقة الرسمية تُختار بعض الفقرات (أجب عن 10 من 12 مثلًا)؛ هنا تتدرب عليها كلها لتقيس نفسك بالكامل.',
  passage: {
    title: 'The Town That Disappeared',
    text: 'In 1995, the small town of Centralia in Pennsylvania had nearly 1,000 residents, a busy main street, and a post office that served the surrounding farms. Today, none of that exists. Centralia is now a ghost town, and only a handful of people still live among its empty streets.\n\nThe change began in 1962, when the local council decided to burn the town\'s rubbish in an open pit near the old mine. The fire was supposed to be controlled, but it quickly spread to an underground coal seam. Nobody could put it out. For decades, the fire burned silently beneath the town, releasing poisonous gases and causing the ground to collapse.\n\nAt first, the residents did not worry. The fire seemed far away, and the temperature underground was not very high. However, in 1979, a petrol station owner noticed that the fuel in his tanks was unusually hot. Tests showed that the temperature of the ground near the station was over 600°C. Worse still, toxic gases were rising through cracks in the road, making people feel dizzy and sick.\n\nBy 1984, engineers warned that the whole town was in danger. The government offered each family a generous amount of money to move away, and most residents accepted. Houses were torn down, and streets cracked open as the ground beneath them gave way. Trees on the surrounding hills turned brown and died because their roots had been cooked underground.\n\nToday, scientists believe the fire will continue to burn for another 250 years. Tourists sometimes visit Centralia to walk on its empty streets and take photographs of the smoke rising from the ground. Some people describe the experience as fascinating; others say it is a sad reminder of how a small mistake can change a community forever.'
  },
  parts: [
    {
      id: 'q1a', label: 'السؤال الأول — A', title: 'قراءة: قطعة غير مرئية', realMarks: 10, choice: 'أجب عن 5 أسئلة فقط في الورقة',
      items: [
        { id: 'r1', type: 'mcq', m: 2, q: 'How many people were living in Centralia in 1995?', opts: ['About 100', 'About 500', 'About 1,000', 'About 10,000'], ans: 2, why: 'من القطعة: "In 1995, the small town of Centralia ... had nearly 1,000 residents."' },
        { id: 'r2', type: 'mcq', m: 2, q: 'Why did the fire start in Centralia?', opts: ['A lightning strike hit the ground.', 'Burning rubbish spread to a coal seam.', 'A petrol station exploded.', 'Miners left candles burning.'], ans: 1, why: 'من القطعة: "decided to burn the town\'s rubbish ... it quickly spread to an underground coal seam."' },
        { id: 'r3', type: 'mcq', m: 2, q: 'What did the petrol station owner notice in 1979?', opts: ['The road outside was cracking.', 'His fuel was unusually hot.', 'His customers were getting sick.', 'The ground was covered in smoke.'], ans: 1, why: 'من القطعة: "noticed that the fuel in his tanks was unusually hot."' },
        { id: 'r4', type: 'mcq', m: 2, q: 'How long do scientists think the fire will continue to burn?', opts: ['Another 50 years', 'Another 100 years', 'Another 250 years', 'Another 500 years'], ans: 2, why: 'من القطعة: "the fire will continue to burn for another 250 years."' },
        { id: 'r5', type: 'mcq', m: 2, q: 'Why were the trees on the hills turning brown and dying?', opts: ['They had no water.', 'Tourists were damaging them.', 'Their roots had been cooked underground.', 'Poisonous gases were killing their leaves.'], ans: 2, why: 'من القطعة: "turned brown and died because their roots had been cooked underground."' },
        { id: 'r6', type: 'tf', m: 1, q: 'Most residents refused to leave Centralia when the government offered them money.', ans: 'F', why: 'خطأ — أغلب السكان قَبِلوا المال وانتقلوا: "most residents accepted".' },
        { id: 'r7', type: 'tf', m: 1, q: 'The ground temperature near the petrol station was over 600°C.', ans: 'T', why: 'صحيح — "the temperature of the ground near the station was over 600°C".' },
        { id: 'r8', type: 'open', m: 2, q: 'In your own words, explain why Centralia is described as "a sad reminder of how a small mistake can change a community forever." (2–3 sentences)', model: 'Centralia is described as a "sad reminder" because the entire town was destroyed by a small mistake made in 1962, when the council decided to burn rubbish near the old mine. What started as a simple, controlled fire turned into a disaster that lasted for decades and forced almost everyone to leave their homes. It shows how one careless decision can have terrible, long-lasting consequences for a whole community.' }
      ]
    },
    {
      id: 'q1b', label: 'السؤال الأول — B', title: 'قراءة: من الكتاب المقرر', realMarks: 10,
      items: [
        { id: 't1', type: 'open', m: 2, tag: 'Unit 1 — Ammar\'s blog', q: 'How did Ammar hurt himself? And how did the doctors help him walk again?', model: 'Ammar hurt himself when he dived into a river from a bridge. The doctors helped him walk again by using an advanced exoskeleton, a robotic device that supported his body and allowed him to stand up and walk.' },
        { id: 't2', type: 'tf', m: 1, tag: 'Unit 2 — Security guard advert', q: 'You must be at least 18 years old to apply for the job.', ans: 'T', why: 'الإعلان ينص: "You must be at least 18 years old to apply for the job".' },
        { id: 't3', type: 'tf', m: 1, tag: 'Unit 2 — Security guard advert', q: 'The job requires you to speak Arabic only.', ans: 'F', why: 'خطأ — المطلوب الإنجليزية والعربية معًا، وليس العربية فقط.' },
        { id: 't4', type: 'mcq', m: 2, tag: 'Unit 3 — Career adviser', q: 'What does the careers adviser suggest if the student is not sure what to study?', opts: ['Choose a popular subject.', 'Talk to a university student.', 'Take a year off to travel.', 'Look at the job advertisements in newspapers.'], ans: 1, why: 'نصيحة مستشار المهنة: التحدث مع طالب جامعي للاستفسار.' },
        { id: 't5', type: 'open', m: 2, tag: 'Unit 4 — Modern fitness article', q: 'According to the article, why is it harder for gym owners nowadays than it used to be?', model: 'It is harder for gym owners nowadays because they now have to compete with home gyms, fitness apps, and online workout programmes. Many people prefer to exercise at home using technology, so gyms have to find new ways to attract customers.' },
        { id: 't6', type: 'tf', m: 1, tag: 'Unit 5 — Kerkennah Islands', q: 'Anna and her cousin travelled to the islands by plane.', ans: 'T', why: 'صحيح — سافرا جويًا إلى الجزر.' },
        { id: 't7', type: 'tf', m: 1, tag: 'Unit 5 — Kerkennah Islands', q: 'The hotel was right next to the beach.', ans: 'F', why: 'خطأ — كان الفندق على بُعد 200 متر من الشاطئ، وليس بجانبه مباشرة.' }
      ]
    },
    {
      id: 'q2a', label: 'السؤال الثاني — A', title: 'أعد الكتابة دون تغيير المعنى', realMarks: 20, choice: 'أجب عن 10 فقرات فقط في الورقة',
      items: [
        { id: 'w1', type: 'rewrite', m: 2, tag: 'Unit 1 — الماضي المستمر والبسيط', q: 'I was reading a book when the phone rang.', arrow: 'While I _______________', model: 'While I was reading a book, the phone rang.' },
        { id: 'w2', type: 'rewrite', m: 2, tag: 'Unit 1 — used to', q: 'When I was a child, I played outside every day.', arrow: 'I _______________ when I was a child.', model: 'I used to play outside every day when I was a child.' },
        { id: 'w3', type: 'rewrite', m: 2, tag: 'Unit 1 — صيغ الكمية', q: "There isn't much milk in the fridge.", arrow: 'There is _______________ milk in the fridge.', model: 'There is very little milk in the fridge.  (أو: only a little)' },
        { id: 'w4', type: 'rewrite', m: 2, tag: 'Unit 2 — أفعال ناقصة', q: 'It is necessary for you to wear a seat belt in the car.', arrow: 'You _______________ wear a seat belt in the car.', model: 'You must wear a seat belt in the car.' },
        { id: 'w5', type: 'rewrite', m: 2, tag: 'Unit 2 — have/get something done', q: 'The mechanic repaired my car yesterday.', arrow: 'I _______________ my car yesterday.', model: 'I had my car repaired yesterday.' },
        { id: 'w6', type: 'rewrite', m: 2, tag: 'Unit 3 — الشرط الأول', q: "I don't have any money, so I can't buy that book.", arrow: 'If I _______________ that book.', model: 'If I had some money, I would / could buy that book.' },
        { id: 'w7', type: 'rewrite', m: 2, tag: 'Unit 3 — الكلام المنقول', q: '"You are working very hard," the teacher said to me.', arrow: 'The teacher told me that _______________', model: 'The teacher told me that I was working very hard.' },
        { id: 'w8', type: 'rewrite', m: 2, tag: 'Unit 3 — wish / if only', q: "I didn't study hard, so I failed the exam.", arrow: 'If only I _______________ the exam.', model: "If only I had studied hard, I wouldn't have failed the exam." },
        { id: 'w9', type: 'rewrite', m: 2, tag: 'Unit 4 — الشرط الثالث', q: "We didn't take a taxi, so we arrived late.", arrow: 'If we _______________ late.', model: "If we had taken a taxi, we wouldn't have arrived late." },
        { id: 'w10', type: 'rewrite', m: 2, tag: 'Unit 5 — المضارع التام مع for', q: 'She started learning French three years ago, and she still studies it.', arrow: 'She _______________ three years.', model: 'She has been learning French for three years.' },
        { id: 'w11', type: 'rewrite', m: 2, tag: 'Unit 6 — المبني للمجهول', q: 'Someone will announce the results next week.', arrow: 'The results _______________ next week.', model: 'The results will be announced next week.' },
        { id: 'w12', type: 'rewrite', m: 2, tag: 'Unit 8 — الشرط الثاني', q: "I don't have a big house, so I can't invite all my friends.", arrow: 'If I _______________ all my friends.', model: 'If I had a big house, I would invite all my friends.' }
      ]
    },
    {
      id: 'q2b', label: 'السؤال الثاني — B', title: 'اختيار من متعدد', realMarks: 10, choice: 'أجب عن 5 فقرات فقط في الورقة',
      items: [
        { id: 'm1', type: 'mcq', m: 2, tag: 'Unit 1', q: 'My back _______ all the time. It only feels OK when I am lying down.', opts: ['hurt', 'hurts', 'is hurting', 'has hurt'], ans: 1, why: 'المضارع البسيط مع المفرد الغائب لحالة متكررة: hurts.' },
        { id: 'm2', type: 'mcq', m: 2, tag: 'Unit 2', q: 'When you get in a car, you _______ put on your seat belt.', opts: ["mustn't", "don't have to", 'must', "needn't"], ans: 2, why: 'must للتعبير عن الوجوب والقانون.' },
        { id: 'm3', type: 'mcq', m: 2, tag: 'Unit 3', q: 'If I _______ a million pounds, I would travel around the world.', opts: ['have', 'had', 'will have', 'have had'], ans: 1, why: 'الشرط الثاني: if + الماضي البسيط.' },
        { id: 'm4', type: 'mcq', m: 2, tag: 'Unit 5', q: 'We _______ each other since we were at primary school.', opts: ['know', 'knew', 'have known', 'had known'], ans: 2, why: 'المضارع التام مع since لحدث بدأ في الماضي وما زال مستمرًا.' },
        { id: 'm5', type: 'mcq', m: 2, tag: 'Unit 6', q: 'This letter _______ by my father yesterday.', opts: ['writes', 'is written', 'was written', 'has been written'], ans: 2, why: 'المبني للمجهول مع زمن ماضٍ محدد: was + التصريف الثالث.' },
        { id: 'm6', type: 'mcq', m: 2, tag: 'Unit 7', q: 'This time next week, I _______ in Spain.', opts: ['will study', 'will be studying', 'study', 'have studied'], ans: 1, why: 'المستقبل المستمر لحدث جارٍ في وقت محدد في المستقبل.' }
      ]
    },
    {
      id: 'q3a', label: 'السؤال الثالث — A', title: 'أكمل الجمل بكلمة من الصندوق', realMarks: 5,
      box: ['deposits', 'instalments', 'renewable', 'calories', 'health', 'evidence', 'salary'],
      items: [
        { id: 'v1', type: 'fill', m: 1, q: 'A doctor advised him to reduce the number of _______ he eats every day to lose weight.', ans: 'calories' },
        { id: 'v2', type: 'fill', m: 1, q: 'Wind and solar power are examples of _______ energy.', ans: 'renewable' },
        { id: 'v3', type: 'fill', m: 1, q: 'The scientists found strong _______ that the water was polluted.', ans: 'evidence' },
        { id: 'v4', type: 'fill', m: 1, q: 'My uncle makes monthly _______ into his savings account at the bank.', ans: 'deposits' },
        { id: 'v5', type: 'fill', m: 1, q: 'The company offered him a high _______ for the new manager position.', ans: 'salary' }
      ]
    },
    {
      id: 'q3b', label: 'السؤال الثالث — B', title: 'طابق الكلمة مع تعريفها', realMarks: 5,
      words: ['a witness', 'a bank statement', 'profit', 'punctual', 'ruins'],
      defs: [
        { k: 'a', t: 'the money that you make in a business' },
        { k: 'b', t: 'a document that shows what happened to your bank account' },
        { k: 'c', t: 'a person who saw or heard something at the time of a crime' },
        { k: 'd', t: 'the remains of an old building' },
        { k: 'e', t: 'always arriving on time' }
      ],
      keys: ['c', 'b', 'a', 'e', 'd'],
      items: [
        { id: 'p1', type: 'match', m: 1, pair: 0 },
        { id: 'p2', type: 'match', m: 1, pair: 1 },
        { id: 'p3', type: 'match', m: 1, pair: 2 },
        { id: 'p4', type: 'match', m: 1, pair: 3 },
        { id: 'p5', type: 'match', m: 1, pair: 4 }
      ]
    },
    {
      id: 'q3c', label: 'السؤال الثالث — C', title: 'الإملاء', realMarks: 10,
      items: [
        { id: 's1', type: 'spell', m: 1, tag: 'لواحق', q: 'The new road __________ (improve) made our journey to school much faster.', ans: ['improvement'] },
        { id: 's2', type: 'spell', m: 1, tag: 'لواحق', q: 'His parents were very proud of his __________ (achieve).', ans: ['achievement'] },
        { id: 's3', type: 'spell', m: 1, tag: 'سوابق', q: "The court found the witness's statement to be __________ (reliable).", ans: ['unreliable'] },
        { id: 's4', type: 'spell', m: 1, tag: 'سوابق', q: 'The students were told to __________ (obey) the school rules.', ans: ['disobey'] },
        { id: 's5', type: 'spell', m: 1, tag: 'أسماء مركبة', q: 'The hotel has its own private __________ (beach + front) where guests can swim.', ans: ['beachfront', 'seafront'] },
        { id: 's6', type: 'spell', m: 1, tag: 'أسماء مركبة', q: 'We had a wonderful __________ (sight + seeing) tour of the old city.', ans: ['sightseeing'] },
        { id: 's7', type: 'spell', m: 1, tag: 'حروف ناقصة', q: 'e_v_d_nc_  (proof)', ans: ['evidence'] },
        { id: 's8', type: 'spell', m: 1, tag: 'حروف ناقصة', q: 'l_br_r_  (place with books)', ans: ['library'] },
        { id: 's9', type: 'spell', m: 1, tag: 'اختصارات', q: 'ATM = ?', ans: ['automated teller machine', 'automatic teller machine'] },
        { id: 's10', type: 'spell', m: 1, tag: 'اختصارات', q: 'PIN = ?', ans: ['personal identification number'] }
      ]
    },
    {
      id: 'q4a', label: 'السؤال الرابع — A', title: 'الأدب: كبرياء وهوى + كما تشاء', realMarks: 10,
      items: [
        { id: 'l1', type: 'tf', m: 1, tag: 'Pride and Prejudice', q: 'Mr Bennet was very enthusiastic about visiting Mr Bingley when his wife first suggested it.', ans: 'F', why: 'لم يكن متحمسًا في البداية؛ كان على زوجته أن تقنعه.' },
        { id: 'l2', type: 'tf', m: 1, tag: 'Pride and Prejudice', q: 'Mr Darcy thought Elizabeth was the only beautiful girl at the ball.', ans: 'T', why: 'قال Darcy إن إليزابيث كانت الوحيدة الجميلة في القاعة.' },
        { id: 'l3', type: 'open', m: 2, tag: 'Pride and Prejudice', q: 'Why did Elizabeth dislike Mr Darcy so strongly, according to the text?', model: 'Elizabeth disliked Mr Darcy strongly because of his rude behaviour at the ball, where he refused to dance with her and said she was not handsome enough to tempt him. In addition, she had heard from Mr Wickham that Mr Darcy had treated him very unfairly, which made her dislike him even more.' },
        { id: 'l4', type: 'tf', m: 1, tag: 'Pride and Prejudice', q: 'Mr Wickham was able to take legal action against Mr Darcy for what he did to him.', ans: 'F', why: 'لم يستطع؛ لأن وصية الأب Darcy لم تكن واضحة قانونيًا بشأن الميراث.' },
        { id: 'l5', type: 'mcq', m: 2, tag: 'As You Like It', q: 'Why did Orlando fight the court wrestler, Charles?', opts: ['Because he wanted to win money.', 'Because Oliver, his brother, told him to.', 'Because Charles insulted him and he had no choice.', 'Because he was angry at the duke.'], ans: 2, why: 'لأن Charles أهانه ولم يكن لديه خيار.' },
        { id: 'l6', type: 'tf', m: 1, tag: 'As You Like It', q: 'Orlando fell in love with Celia.', ans: 'F', why: 'خطأ — وقع Orlando في حب Rosalind؛ أما Oliver فقد تزوج Celia.' },
        { id: 'l7', type: 'tf', m: 1, tag: 'As You Like It', q: 'Rosalind disguised herself as a young man named Ganymede.', ans: 'T', why: 'صحيح — تنكرت Rosalind بشاب اسمه Ganymede.' },
        { id: 'l8', type: 'open', m: 1, tag: 'As You Like It', q: 'How did Oliver change at the end of the play?', model: 'At the end of the play, Oliver changed from being a cruel and jealous brother into a kind and loving one. He was saved by Orlando from a lioness, and this experience made him realise how wrong he had been. He even fell in love with Celia and married her.' }
      ]
    },
    {
      id: 'q4b', label: 'السؤال الرابع — B', title: 'ابحث عن الكلمة في النص', realMarks: 5,
      items: [
        { id: 'f1', type: 'find', m: 1, tag: 'Pride and Prejudice', q: 'a very large amount of money = f ______', ans: ['fortune'] },
        { id: 'f2', type: 'find', m: 1, tag: 'Pride and Prejudice', q: 'someone who is no longer alive = the d ______', ans: ['the deceased', 'deceased'] },
        { id: 'f3', type: 'find', m: 1, tag: 'As You Like It', q: 'the person who fights another in a competition = a w ______', ans: ['a wrestler', 'wrestler'] },
        { id: 'f4', type: 'find', m: 1, tag: 'As You Like It', q: 'a woman who serves in a royal house = a l ______', ans: ['a lady', 'lady'] },
        { id: 'f5', type: 'find', m: 1, tag: 'As You Like It', q: 'a powerful army = an ______', ans: ['army'] }
      ]
    },
    {
      id: 'q5', label: 'السؤال الخامس', title: 'الكتابة (اختر موضوعًا واحدًا)', realMarks: 15,
      items: [
        {
          id: 'e1', type: 'essay', m: 15,
          topics: [
            { title: 'Topic A — The Importance of Education', prompt: 'In your opinion, why is education important for young people today? Write a short essay (100–120 words) discussing the benefits of education. Include: the role of education in finding a good job · how education helps people develop as individuals · one other benefit of your choice.', model: 'Education is one of the most important things in a young person\'s life, and it brings many benefits. Firstly, education helps people find good jobs. In today\'s world, almost every job requires some kind of qualification, and people who study hard usually have more opportunities than those who do not.\n\nSecondly, education is not only about getting a job; it also helps people develop as individuals. When students study different subjects, they learn how to think, how to solve problems, and how to communicate with others. These skills are useful in every part of life, not just at work.\n\nFurthermore, education helps build a better society. When people are educated, they make better decisions, they understand their rights, and they can help their communities grow. For all these reasons, I believe that education is the key to a successful future, and every young person should take it seriously.' },
            { title: 'Topic B — Protecting Our Environment', prompt: 'Many people say that protecting the environment is everyone\'s responsibility. Do you agree? Write a short essay (100–120 words) discussing ways in which individuals and governments can protect the environment. Include: one thing families can do at home · one thing schools can do · one thing the government can do.', model: 'I strongly agree that protecting the environment is everyone\'s responsibility, and there are many things that families, schools, and governments can do to help.\n\nAt home, families can reduce, reuse, and recycle. For example, they can use fewer plastic bags, turn off the lights when they leave a room, and save water by taking shorter showers. These small actions, when done by millions of families, can have a huge effect.\n\nSchools also have an important role to play. They can teach students about the environment and encourage them to plant trees, clean up their neighbourhoods, and join environmental clubs. When children learn about protecting nature at a young age, they will grow up to be responsible adults.\n\nFinally, the government should pass stricter laws to reduce pollution, support clean energy, and protect forests and wildlife. In my opinion, if everyone works together — families, schools, and the government — we can make our planet a cleaner and healthier place to live.' }
          ],
          criteria: [
            'إنجاز المهمة (يغطي النقاط المطلوبة) — 5 درجات',
            'التنظيم (مقدمة وعرض وخاتمة) — 4 درجات',
            'دقة اللغة (قواعد ومفردات وإملاء) — 4 درجات',
            'الربط والانسجام (روابط وتسلسل منطقي) — درجتان'
          ]
        }
      ]
    }
  ]
};
