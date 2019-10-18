import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")


def preprocess_reviews(reviews):
	reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
	reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]

	return reviews


# 파일 읽기
reviews_train = []
for line in open('movie_data/full_train.txt', 'r', encoding='UTF-8'):
	reviews_train.append(line.strip())

reviews_test = []
for line in open('movie_data/full_test.txt', 'r', encoding='UTF-8'):
	reviews_test.append(line.strip())

# 문장 전처리 (특수문자 등 제거)
reviews_train_clean = preprocess_reviews(reviews_train)
reviews_test_clean = preprocess_reviews(reviews_test)

# 벡터화
cv = CountVectorizer(binary=True)
cv.fit(reviews_train_clean)
X = cv.transform(reviews_train_clean)
X_test = cv.transform(reviews_test_clean)

for i in range(25000):
	if i < 12500:
		a = 1
	else:
		a = 0

# 분류기 구축
target = [1 if i < 12500 else 0 for i in range(25000)]
X_train, X_val, y_train, y_val = train_test_split(X, target, train_size=0.75)

# 정확도 측정?
# for c in [0.01, 0.05, 0.25, 0.5, 1]:
# 	lr = LogisticRegression(C=c)
# 	lr.fit(X_train, y_train)
# 	print("Accuracy for C=%s: %s" % (c, accuracy_score(y_val, lr.predict(X_val))))
# 	# 0.05 가 제일 놓음

# 최종 모델 훈련
final_model = LogisticRegression(C=0.05)
final_model.fit(X, target)
print("Final Accuracy : %s" % accuracy_score(target, final_model.predict(X_test)))
# 최종 정확도 : 0.88128

feature_to_coef = {
	word: coef for word, coef in zip(cv.get_feature_names(), final_model.coef_[0])
}

for best_positive in sorted(feature_to_coef.items(), key=lambda x: x[1], reverse=True)[:5]:
	print(best_positive)

for best_negative in sorted(feature_to_coef.items(), key=lambda x: x[1])[:5]:
	print(best_negative)