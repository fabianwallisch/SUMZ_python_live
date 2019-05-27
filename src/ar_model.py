from statsmodels.tsa.ar_model import AR
import numpy as np


def predict(time_series, pred_steps, num_samples):
    result = []

    for x in range(len(time_series)):
        result.append({})
        result[x]['id'] = time_series[x]['id']
        result[x]['preds'] = []

        train_series = np.array(time_series[x]['values'])

        ar = AR(train_series)
        ar_fit = ar.fit(
            maxlag=min(len(train_series) - 1, round(12*(len(train_series)/100.)**(1/4.))),
            ic='aic',
            maxiter=200
        )

        coeff = ar_fit.params
        epsilon_mean = 0
        epsilon_std = ar_fit.resid.std()
        random = np.random.RandomState(1234567890)

        print(coeff)
        print(epsilon_std)

        for i in range(num_samples):
            preds = np.zeros(pred_steps + len(coeff) - 1)
            preds[:len(coeff) - 1] = train_series[-len(coeff) + 1:]

            epsilon = random.normal(loc=epsilon_mean, scale=epsilon_std)
            print("Epsilon: ", epsilon)

            for j in range(len(coeff) - 1, len(coeff) - 1 + pred_steps):
                preds[j] = np.dot(preds[j-len(coeff)+1:j], np.flip(coeff[1:], axis=0)) + coeff[0] + epsilon

            print("Preds: ", preds)
            result[x]['preds'].append(list(preds[len(coeff)-1:]))

    return result