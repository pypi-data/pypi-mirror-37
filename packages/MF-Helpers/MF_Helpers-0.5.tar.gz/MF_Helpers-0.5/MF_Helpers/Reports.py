import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import precision_score, recall_score, auc, roc_curve, precision_recall_fscore_support


def __init__(self):
		''' Constructor for this class. '''
		
# расширенный classification report, который корректно работает для мультиклассовых моделей
def classification_report(y_true, y_pred, y_score=None, average='micro'):
	if y_true.shape != y_pred.shape:
		print("Error! y_true %s is not the same shape as y_pred %s" % (
			  y_true.shape,
			  y_pred.shape)
		)
		return

	lb = LabelBinarizer()

	if len(y_true.shape) == 1:
		lb.fit(y_true)

	#Value counts of predictions
	labels, cnt = np.unique(
		y_pred,
		return_counts=True)
	n_classes = len(labels)
	pred_cnt = pd.Series(cnt, index=labels)

	metrics_summary = precision_recall_fscore_support(
			y_true=y_true,
			y_pred=y_pred,
			labels=labels)

	avg = list(precision_recall_fscore_support(
			y_true=y_true, 
			y_pred=y_pred,
			average='weighted'))

	metrics_sum_index = ['precision', 'recall', 'f1-score', 'support']
	class_report_df = pd.DataFrame(
		list(metrics_summary),
		index=metrics_sum_index,
		columns=labels)

	support = class_report_df.loc['support']
	total = support.sum() 
	class_report_df['avg / total'] = avg[:-1] + [total]

	class_report_df = class_report_df.T
	class_report_df['pred'] = pred_cnt
	class_report_df['pred'].iloc[-1] = total

	if not (y_score is None):
		fpr = dict()
		tpr = dict()
		roc_auc = dict()
		for label_it, label in enumerate(labels):
			fpr[label], tpr[label], _ = roc_curve(
				(y_true == label).astype(int), 
				y_score[:, label_it])

			roc_auc[label] = auc(fpr[label], tpr[label])

		if average == 'micro':
			if n_classes <= 2:
				fpr["avg / total"], tpr["avg / total"], _ = roc_curve(
					lb.transform(y_true).ravel(), 
					y_score[:, 1].ravel())
			else:
				fpr["avg / total"], tpr["avg / total"], _ = roc_curve(
						lb.transform(y_true).ravel(), 
						y_score.ravel())

			roc_auc["avg / total"] = auc(
				fpr["avg / total"], 
				tpr["avg / total"])

		elif average == 'macro':
			# First aggregate all false positive rates
			all_fpr = np.unique(np.concatenate([
				fpr[i] for i in labels]
			))

			# Then interpolate all ROC curves at this points
			mean_tpr = np.zeros_like(all_fpr)
			for i in labels:
				mean_tpr += interp(all_fpr, fpr[i], tpr[i])

			# Finally average it and compute AUC
			mean_tpr /= n_classes

			fpr["macro"] = all_fpr
			tpr["macro"] = mean_tpr

			roc_auc["avg / total"] = auc(fpr["macro"], tpr["macro"])

		class_report_df['AUC'] = pd.Series(roc_auc)

	return class_report_df
	
# получение сегмента АРПУ
def get_arpu_segment(arpu):
	if (arpu < 100):
		return 1
	if ((arpu >= 100) & (arpu < 300)):
		return 2
	if ((arpu >= 300) & (arpu < 700)):
		return 3
	if ((arpu >= 700) & (arpu < 1000)):
		return 4
	if (arpu >= 1000):
		return 5

# расширенные classification report, сформированные для всех сегментов АРПУ и отдельно для train/test
def classification_reports(y_train, x_train, y_test, x_test, arpu_segment_train, arpu_segment_test, model):
	reports = {}
	
	pred_train = model.predict(x_train)
	pred_test = model.predict(x_test)
	score_train = model.predict_proba(x_train)
	score_test = model.predict_proba(x_test)
	
	arpu_segment_test.reset_index(drop=True, inplace=True)
	y_test.reset_index(drop=True, inplace=True)
	
	arpu_segment_train.reset_index(drop=True, inplace=True)
	y_train.reset_index(drop=True, inplace=True)
	
	#general report
	reports[0] = {}
	reports[0]["test"] = classification_report(y_test, pred_test, score_test)
	reports[0]["train"] = classification_report(y_train, pred_train, score_train)

	#reports by ARPU segments
	for i in np.arange(1, 6):
		reports[i] = {}
		reports[i]["test"] = classification_report(y_test[arpu_segment_test.index[arpu_segment_test == i]],
												   pred_test[arpu_segment_test.index[arpu_segment_test == i]],
												   score_test[arpu_segment_test.index[arpu_segment_test == i], :])
		reports[i]["train"] = classification_report(y_train[arpu_segment_train.index[arpu_segment_train == i]],
													pred_train[arpu_segment_train.index[arpu_segment_train == i]],
													score_train[arpu_segment_train.index[arpu_segment_train == i], :])
	return reports			

# отчет по сегментам АРПУ для различных границ
def report_with_thresholds(fact_train, pred_train, arpu_segment_train, fact_test, pred_test, arpu_segment_test):
	
	res = pd.DataFrame({'segment_ARPU': np.repeat(['Extra Low', 'General Low', 'Medium', 'General High', 'Extra High'], 4),
						'top': [10, 20, 30, 40] * 5,
						'precision_train': .0,
						'recall_train': .0,
						'precision_test': .0,
						'recall_test': .0,
						'threshold_train': .0,
						'threshold_test': .0})

	df_test = pd.DataFrame(
		{
			'arpu_segment' : arpu_segment_test.reset_index(drop=True),
			'fact' : fact_test.reset_index(drop=True),
			'pred' : pred_test.reset_index(drop=True)
		})
	
	df_train = pd.DataFrame(
		{
			'arpu_segment' : arpu_segment_train.reset_index(drop=True),
			'fact' : fact_train.reset_index(drop=True),
			'pred' : pred_train.reset_index(drop=True)
		})

	for i in np.arange(1, 6):
		f_test = df_test.loc[df_test.arpu_segment == i].fact
		p_test = df_test.loc[df_test.arpu_segment == i].pred
		f_train = df_train.loc[df_train.arpu_segment == i].fact
		p_train = df_train.loc[df_train.arpu_segment == i].pred

		for j in np.arange((i-1)*4, i*4):
			res.at[j, 'precision_train'] = precision_score(f_train, p_train >= np.percentile(p_train, 100-res.at[j, 'top']))
			res.at[j, 'recall_train'] = recall_score(f_train, p_train >= np.percentile(p_train, 100-res.at[j, 'top']))
			res.at[j, 'precision_test'] = precision_score(f_test, p_test >= np.percentile(p_test, 100-res.at[j, 'top']))
			res.at[j, 'recall_test'] = recall_score(f_test, p_test >= np.percentile(p_test, 100-res.at[j, 'top']))
			res.at[j, 'threshold_train'] = np.percentile(p_train, 100-res.at[j, 'top'])
			res.at[j, 'threshold_test'] = np.percentile(p_test, 100-res.at[j, 'top'])
	
	return res		
	
# отчеты по сегментам АРПУ для различных границ по всем классам
def reports_with_thresholds(y_train, x_train, y_test, x_test, arpu_segment_train, arpu_segment_test, model):
	
	levels = y_train.append(y_test).unique()
	
	pred_train = pd.DataFrame(model.predict_proba(x_train)
							  , columns=model.classes_)
	pred_test = pd.DataFrame(model.predict_proba(x_test)
							 , columns=model.classes_)

	reports = {}

	for l in levels:
		y_train_l = y_train.copy()
		y_test_l = y_test.copy()
	
		y_train_l[y_train_l == l] = -100
		y_train_l[y_train_l != -100] = 0
		y_train_l[y_train_l == -100] = 1
	
		y_test_l[y_test_l == l] = -100
		y_test_l[y_test_l != -100] = 0
		y_test_l[y_test_l == -100] = 1
	
		reports[l] = report_with_thresholds(fact_train = y_train_l,
											pred_train = pred_train.loc[:, l],
											arpu_segment_train = arpu_segment_train,
											fact_test = y_test_l,
											pred_test = pred_test.loc[:, l],
											arpu_segment_test = arpu_segment_test)
	
	return reports
	
def auc_report(class_reports, levels):    
	report = pd.DataFrame({'segment_ARPU': ['Extra Low', 'General Low', 'Medium', 'General High', 'Extra High'],
						   'AUC_train, avg': .0,
						   'AUC_test, avg':.0})
	for l in levels:
		report = pd.concat([report.reset_index(drop=True),
							pd.DataFrame({'AUC_train, class ' + str(l) : [0.0, 0.0, 0.0, 0.0, 0.0],
										  'AUC_test, class ' + str(l) : [0.0, 0.0, 0.0, 0.0, 0.0]})],
						   axis = 1)

	for i in np.arange(1, 6):
		report.at[i - 1, 'AUC_train, avg'] = class_reports[i]["train"].AUC[len(levels)]
		report.at[i - 1, 'AUC_test, avg'] = class_reports[i]["test"].AUC[len(levels)]
		for l in levels:
			report.at[i - 1, 'AUC_train, class ' + str(l)] = class_reports[i]["train"].AUC[l]
			report.at[i - 1, 'AUC_test, class ' + str(l)] = class_reports[i]["test"].AUC[l]
	
	return report

def precision_report(class_reports, levels):
	report = pd.DataFrame({'segment_ARPU': ['Extra Low', 'General Low', 'Medium', 'General High', 'Extra High'],
						   'Precision_train, avg': .0,
						   'Precision_test, avg':.0})
	for l in levels:
		report = pd.concat([report.reset_index(drop=True),
							pd.DataFrame({'Precision_train, class ' + str(l) : [0.0, 0.0, 0.0, 0.0, 0.0],
										  'Precision_test, class ' + str(l) : [0.0, 0.0, 0.0, 0.0, 0.0]})],
						   axis = 1)

	for i in np.arange(1, 6):
		report.at[i - 1, 'Precision_train, avg'] = class_reports[i]["train"].precision[len(levels)]
		report.at[i - 1, 'Precision_test, avg'] = class_reports[i]["test"].precision[len(levels)]
		for l in levels:
			report.at[i - 1, 'Precision_train, class ' + str(l)] = class_reports[i]["train"].precision[l]
			report.at[i - 1, 'Precision_test, class ' + str(l)] = class_reports[i]["test"].precision[l]
	
	return report		
	
def recall_report(class_reports, levels):
	report = pd.DataFrame({'segment_ARPU': ['Extra Low', 'General Low', 'Medium', 'General High', 'Extra High'],
						   'Recall_train, avg': .0,
						   'Recall_test, avg':.0})
	for l in levels:
		report = pd.concat([report.reset_index(drop=True),
							pd.DataFrame({'Recall_train, class ' + str(l) : [0.0, 0.0, 0.0, 0.0, 0.0],
										  'Recall_test, class ' + str(l) : [0.0, 0.0, 0.0, 0.0, 0.0]})],
						   axis = 1)

	for i in np.arange(1, 6):
		report.at[i - 1, 'Recall_train, avg'] = class_reports[i]["train"].recall[len(levels)]
		report.at[i - 1, 'Recall_test, avg'] = class_reports[i]["test"].recall[len(levels)]
		for l in levels:
			report.at[i - 1, 'Recall_train, class ' + str(l)] = class_reports[i]["train"].recall[l]
			report.at[i - 1, 'Recall_test, class ' + str(l)] = class_reports[i]["test"].recall[l]
	
	return report
	
def f1_report(class_reports, levels):
	report = pd.DataFrame({'segment_ARPU': ['Extra Low', 'General Low', 'Medium', 'General High', 'Extra High'],
						   'f1_train, avg': .0,
						   'f1_test, avg':.0})
	for l in levels:
		report = pd.concat([report.reset_index(drop=True),
							pd.DataFrame({'f1_train, class ' + str(l) : [0.0, 0.0, 0.0, 0.0, 0.0],
										  'f1_test, class ' + str(l) : [0.0, 0.0, 0.0, 0.0, 0.0]})],
						   axis = 1)

	for i in np.arange(1, 6):
		report.at[i - 1, 'f1_train, avg'] = class_reports[i]["train"]['f1-score'][len(levels)]
		report.at[i - 1, 'f1_test, avg'] = class_reports[i]["test"]['f1-score'][len(levels)]
		for l in levels:
			report.at[i - 1, 'f1_train, class ' + str(l)] = class_reports[i]["train"]['f1-score'][l]
			report.at[i - 1, 'f1_test, class ' + str(l)] = class_reports[i]["test"]['f1-score'][l]
	
	return report
	
def percentage_report(y_train, y_test, arpu_segment_train, arpu_segment_test):
	levels = y_train.append(y_test).unique()
	
	report = pd.DataFrame({'segment_ARPU': ['Extra Low', 'General Low', 'Medium', 'General High', 'Extra High']})
	for l in levels:
		report = pd.concat([report.reset_index(drop=True),
							pd.DataFrame({'%_train, class ' + str(l) : [0.0, 0.0, 0.0, 0.0, 0.0],
										  '%_test, class ' + str(l) : [0.0, 0.0, 0.0, 0.0, 0.0]})],
						   axis = 1)

	for i in np.arange(1, 6):
		y_train_i = y_train[arpu_segment_train.index[arpu_segment_train == i]]
		y_test_i = y_test[arpu_segment_test.index[arpu_segment_test == i]]
		
		for l in levels:
			report.at[i - 1, '%_train, class ' + str(l)] = len(y_train_i[y_train_i == l])/len(y_train_i)
			report.at[i - 1, '%_test, class ' + str(l)] = len(y_test_i[y_test_i == l])/len(y_test_i)
	
	return report
	
def reports(y_train, x_train, y_test, x_test, arpu_train, arpu_test, model):
	levels = y_train.append(y_test).unique()
	arpu_segment_train = arpu_train.apply(get_arpu_segment)
	arpu_segment_test = arpu_test.apply(get_arpu_segment)
	
	reports = {}
	class_reports = classification_reports(y_train, x_train, y_test, x_test, arpu_segment_train, arpu_segment_test, model)
	
	reports['classification_reports'] = class_reports
	reports['reports_with_thresholds'] = reports_with_thresholds(y_train, x_train, y_test, x_test,
																 arpu_segment_train, arpu_segment_test, model)
	reports['auc_report'] = auc_report(class_reports, levels)
	reports['precision_report'] = precision_report(class_reports, levels)
	reports['recall_report'] = recall_report(class_reports, levels)
	reports['f1_report'] = f1_report(class_reports, levels)
	reports['percentage_report'] = percentage_report(y_train, y_test, arpu_segment_train, arpu_segment_test)
	
	return reports