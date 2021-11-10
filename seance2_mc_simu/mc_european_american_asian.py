def european_mc(T, N, S, r, sigma, K, typeCP = "call"):
  import numpy as np
  if typeCP == "call":
    typeCP = 1
  else :
    typeCP = -1
  z = np.random.randn(N)
  
  ST = S * np.exp((r -0.5 * sigma **2)* T + sigma * np.sqrt(T)*z)
  
  OptionT = np.maximum(typeCP *(ST - K), 0)
  option = np.exp(-r*T)*OptionT.mean()
  return option


def asian_mc(T, N, steps, S, r, sigma, K, typeCP = "call"):
  import numpy as np
  if typeCP == "call":
    typeCP = 1
  else :
    typeCP = -1
  dt = np.float(T)/steps
  SPath = np.zeros((steps+1, N))
  SPath[0] = S
  for t in range (1 , steps +1):
    z = np.random.randn(N)
    SPath[t] = SPath[t-1]* np.exp((r -0.5* sigma **2) * dt + sigma * np.sqrt(dt)* z)
  OptionT = np.maximum(typeCP *(SPath.mean(axis =0) - K), 0)
  option = np.exp(-r*T)*OptionT.mean()
  return option


def american_mc(T,N,steps,S,r,sigma,K, typeCP):
  import numpy as np
	if typeCP=="call":
		typeCP=1
	else:
		typeCP=-1
	
	dt = np.float(T) / steps
	df = np.exp(-r * dt)
	# simulation of index levels
	SPath = np.zeros((steps + 1, N))
	SPath[0] = S
	
	z=np.random.randn(steps,N)

	for t in range(1, steps + 1):
		SPath[t] = SPath[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) *z[t-1])

	# case-based calculation of payoff
	h = np.maximum(typeCP*(SPath - K), 0)
	# LSM algorithm
	V = np.copy(h)
	for t in range(steps - 1, 0, -1):
		reg = np.polyfit(SPath[t], V[t + 1] * df, 7)
		C = np.polyval(reg, SPath[t])
		V[t] = np.where(C > h[t], V[t + 1] * df, h[t])
	# MCS estimator
	option = df * 1 / N * np.sum(V[1])
	return option
