system_prompt="""You are a doctor. Your job is to summarize doctor/patient conversations using the SOAP format (Subjective Objective Assessment Plan) in the following sections: 
## 1. Subjective – The “history” section
- Include symptom dimensions, chronological narrative of patient’s complains, and information obtained from other sources (always identify source if not the patient).
- Pertinent past medical history.
- Pertinent review of body parts, for example, “Patient has not had any stiffness or loss of motion of other joints.”
- Current medications (list with daily dosages).
## 2. Objective - any empirical or quantitative measurements observed during the visit. If none were observed, write \"N/A\"
- difficulty speaking
- vital signs/observations at clinic
## 3. Assessment/Problem List – Your assessment of the patient’s problems
- Assessment: A one sentence description of the patient\'s chief complaint and any potential diagnoses found in the text. If there was no diagnosis, write \"N/A\"
### Problem list: A numerical list of problems identified. All listed problems need to be supported by findings in subjective and objective areas above. 
## 4. Plan - the care plan and next steps for the patient. If there are no next steps identified in the text, write \"N/A\"
- Any tests ordered
- Any recommendations for the patient to try next.

Output all text in Markdown format. """
few_shot_1 ="""
input: D: What brings you in today?

P: Yeah, I brought my son here. I\'m a little bit worried about him because like yesterday he had he had this temperature of like 38.5 um so he\'s been feeling a little bit hot and he\'s not swallowing his food, like we\'ve been feeding him some mashed up food but he\'s not swallowing it. He\'s just kind of throwing throwing it back out there. Um he\'s drooling now uh and he sounds kind of muffled um and he\'s been very short of breath.

D: That doesn\'t sound good. Um uh yeah, I\'m I\'m currently looking at him and he doesn\'t uh look great. While the uh while the doctor\'s um taking his vitals and examining the baby, I\'ll just ask you a couple of questions.

P: Sure

D: So you said that all of this started about a day ago. How was he doing before that?

P: He was fine before that, he had like a an infection, like some sort of viral infection recently, like about a week back, he had like a runny nose and a cough, but that went away.

D: Um OK, so he had these symptoms about a week ago. Did he see any, did you take him to the hospital or to a clinic?

P: I took him to our family doctor um and they just suggested some supportive treatments um which we\'ve been doing at home like we try to keep him well hydrated, and we\'ve been keeping an eye on his like um diapers and things like that.

D: OK, has he been um has he been, how many diapers is he um, are you changing a day?

P: Usually like about 5, 6, but yesterday it was like 2.

D: OK. Um and uh has he been uh irritable or agitated?

P: Uh he has been very irritable and fussy.

D: Has he been sleeping OK?

P: I um no you know what last night he didn\'t sleep well at all. He was crying the whole night.

D: Um and uh in terms of uh, so how much has he has he had to eat or drink in the past uh day or two?

P: Uh he\'s had about like maybe a bottle of his milk, like of that.

D: OK.

P: Yeah.

D: That\'s it?

P: Yeah, he\'s not taking. He\'s not he\'s not taking anything else like he\'s been so fussy and so like he\'s unwilling to try anything.

D: OK, um and, OK. Do you feel like he\'s been drowsy uh and um lethargic?

P: Um yeah, I feel like he\'s been a little bit lethargic. Like today, he\'s more lethargic. All of yesterday, he was very fussy and irritable, but today seems like, he\'s very slow.

D: OK, and just a couple of questions about um his past medical history. Does he have any uh medical conditions uh that he was diagnosed with?

P: Uh no, he\'s been healthy otherwise.

D: How was your pregnancy with him?

P: Normal, yeah no complications there.

D: Did did you have GBS or gestational diabetes? 

P: No.

D: No, OK. Did you have any viral infections during that time, during pregnancy?

P: No, no.

D: OK. Any complications during birth?

P: No.

D: Was he um kept in the hospital for a couple days in the NICU after he was born?

P: No. 

D: Did he develop jaundice? 

P: No.

D: OK, and and he\'s been OK for the past two years? Any concerns about his growth, his height and weight, and his head circumference? Has your family doctor uh said anything about that?

P: No, he\'s been pretty good. Um he\'s been growing and gaining weight OK.

D: Any um developmental issues?

P: No.

D: OK, alright, and any medical conditions that run in the family?

P: Uh no, just like some heart issues.

D: Um OK, and uh does he, I forgot to ask, has he had any hospitalizations in the past?

P: No.

D: Any surgeries?

P: No surgeries.

D: Uh has he been on any medications? Any antibiotics recently?

P: No.

D: OK. Has um has he been vaccinated? Uh has his vaccinations, immunizations up to date?

P: Yeah, they\'re all up to date so far.

D: OK, alright, that\'s that\'s good. Um OK, and does he have any allergies that you\'re aware of?

P: Pardon me?

D: Any allergies?

P: Oh, uh no allergies.

D: OK alright um well it looks like um I, it\'s great that you brought him into the emergency room. Um if he hasn\'t been eating, drinking well, hasn\'t slept well, has been fussy, and and has been lethargic and tired, uh and is having difficulty swallowing food, um that\'s definitely very um serious. Uh we\'ll have a look inside his mouth and see what\'s going on. It could be that he has an infection or an inflammation of some sort. Um given his fever, he probably has an infection, um and uh we\'ll likely start him on antibiotics and put in an IV drip just to get in get some fluids inside him, just to get him hydrated, uh and monitor him very closely. We\'ll also check his vitals and um we\'ll do uh, yeah, we\'ll go from there. Do you have any questions?

P: Uh no, thank you. 

D: OK.
output: 
## 1. Subjective:
- Reason for visit: The patient\'s son has a fever of 38.5 and no appetite since yesterday. Previous viral infection a week ago. Patient is irritable and fussy. No allergies, pregnancy complications, or medical conditions. Family history of heart disease.  
- Current medications: None
## 2. Objective: 
- Patient appears lethargic
## 3. Assessment: 
- Potential infection
### Problem list:
- Fever
- Loss of appetite
- Difficulty swallowing
- Lethargy
## 4. Plan: 
- Start patient on antibiotics
- Administer IV fluid drip
- Check vitals
- Monitor for worsening symptoms"""
few_shot_2 = """
input: D: What brought you in today?

P: Sure, I\'m I\'m just having a lot of chest pain and and so I thought I should get it checked out.

D: OK, before we start, could you remind me of your gender and age? 

P: Sure 39, I\'m a male.

D: OK, and so when did this chest pain start?

P: It started last night, but it\'s becoming sharper.

D: OK, and where is this pain located? 

P: It\'s located on the left side of my chest.

D: OK, and, so how long has it been going on for then if it started last night?

P: So I guess it would be a couple of hours now, maybe like 8.

D: OK. Has it been constant throughout that time, or uh, or changing? 

P: I would say it\'s been pretty constant, yeah.

D: OK, and how would you describe the pain? People will use words sometimes like sharp, burning, achy. 

P: I\'d say it\'s pretty sharp, yeah.

D: Sharp OK. Uh, anything that you have done tried since last night that\'s made the pain better?

P: Um not laying down helps.

D: OK, so do you find laying down makes the pain worse?

P: Yes, definitely.

D: OK, do you find that the pain is radiating anywhere?

P: No.

D: OK, and is there anything else that makes the pain worse besides laying down? 

P: Not that I\'ve noticed, no.

D: OK, so not like taking a deep breath or anything like that?

P: Maybe taking a deep breath. Yeah.

D: OK. And when the pain started, could you tell me uh, could you think of anything that you were doing at the time?

P: I mean, I was moving some furniture around, but, that I\'ve done that before.

D: OK, so you didn\'t feel like you hurt yourself when you were doing that?

P: No.

D: OK, and in regards to how severe the pain is on a scale of 1 to 10, 10 being the worst pain you\'ve ever felt, how severe would you say the pain is?

P: I\'d say it\'s like a seven or eight. It\'s pretty bad.

D: OK, and with the pain, do you have any other associated symptoms?

P: I feel a little lightheaded and I\'m having some trouble breathing.

D: OK. Have you had any loss of consciousness?

P: No.

D: OK. Uh, have you been experiencing any like racing of the heart? 

P: Um, a little bit, yeah.

D: OK. And have you been sweaty at all?

P: Just from the from having issues breathing.

D: OK, have you been having issues breathing since the pain started? 

P: Yes.

D: OK. Um recently have you had any periods of time where you like have been immobilized or or, you haven\'t been like able to move around a lot?

P: No no. 

D: OK. And have you been feeling sick at all? Any infectious symptoms? 

P: No. 

D: OK, have you had any nausea or vomiting? 

P: No. 

D: Any fevers or chills?

P: No. 

D: OK, how about any abdominal pain?

P: No.

D: Any urinary problems?

P: No.

D: Or bowel problems?

P: No.

D: OK, have you had a cough?

P: No.

D: OK. You haven\'t brought up any blood?

P: No. 

D: OK, have you had a wheeze with your difficulty breathing?

P: No, not that I\'ve heard.

D: OK, any changes to the breath sounds at all like any noisy breathing?

P: No. Well, I guess if when I\'m really having trouble breathing, yeah.

D: OK. Has anything like this ever happened to you before?

P: No. 

D: No, OK. And have you had any night sweats?

P: No. 

D: Alright, and then how about any rashes or skin changes?

P: No rashes, but I guess like my neck seems to be a little swollen. 

D: OK, do you have any neck pain? 

P: No. 

D: OK, have you had any like accidents like a car accident or anything where you really jerked your neck? 

P: No.

D: OK. Um any any trauma at all to the chest or or back?

P: No.

D: OK, so just in regards to past medical history, do you have any prior medical conditions? 

P: No.

D: OK, any recent hospitalizations?

P: No. 

D: OK, any prior surgeries?

P: No.

D: OK, do you take any medications regularly? Are they prescribed or over the counter?

P: No. 

D: Alright, how about any allergies to medications? 

P: None.

D: Alright, any immunizations or are they up to date? 

P: They are all up to date.

D: Excellent. Alright, and could you tell me a little bit about your living situation currently? 

P: Sure, I live in an apartment by myself. I, uh, yep, that\'s about it.

D: OK, and how do you support yourself financially?

P: I\'m an accountant.

D: OK, sounds like a pretty stressful job or that it can be. Do you smoke cigarettes? 

P: I do.

D: OK, and how much do you smoke?

P: I smoke about a pack a day.

D: OK, how long have you been smoking for?

P: For the past 10 to 15 years.

D: OK. And do you drink alcohol?

P: I do.

D: OK. How much alcohol do you drink each week?

P: Uhm about I would say I have like one or two drinks a day, so about 10 drinks a week. 

D: OK, uh, yeah and um alright, and then briefly, could you tell me a little bit about your like diet and exercise?

P: Sure, I try to eat healthy for dinner at least, but most of my lunches are, uh I eat out. And then in terms of exercise, I try to exercise every other day, I run for about half an hour.

D; OK, well that\'s great that you\'ve been working on the the activity and the diet as well. So has anything like this happened in your family before?

P: No. 

D: OK, has anybody in the family had a heart attack before?

P: Actually, yes, my father had a heart attack when he was 45.

D: OK, and anybody in the family have cholesterol problems?

P: I think my father did.

D: I see OK, and how about anybody in the family have a stroke?

P: No strokes.

D: OK, and then any cancers in the family?

P: No.

D: OK, and is there anything else that you wanted to tell me about today that that I on on history? 

P: No, I don\'t think so. I think you asked me everything.
output: 
## 1. Subjective
- Reason for visit: The patient complains of chest pain, starting last night and increasing today. Patient feels slightly lightheaded, and feels more pain when lying down. He does not have fever, nausea, or vomiting. He does not have abdominal pain. He is a smoker and moderate drinker. There is a family history of heart disease. 
- Current medications: None
## 2. Objective: N/A
## 3. Assessment: 
- Patient with a history of smoking is experiencing sudden onset of chest pain. 
### Problem list: 
- Chest pain
- Lightheadedness
- Swollen neck 
## 4. Plan: N/A"""
end="""
input: {input_text}

output:
"""