def binomialtree(T,N,S,r,sigma,K, typeEA, typeCP):

	if typeCP=="call":
		typeCP=1
	else:
		typeCP=-1	# put

	dt=np.float(T)/N # step size, length of step in tree
	u=np.exp(sigma*np.sqrt(dt)) # up and down steps
	d=1/u
	p=(np.exp(r*dt)-d)/(u-d)

	ST=np.zeros(N+1)
	option=np.zeros(N+1)

	for i in range(0,N+1):
		ST[i]=S*u**(N-i)*d**i
		option[i]=max(typeCP*(ST[i]-K),0)# pay off at the end
	
	for i in range(N-1,-1,-1):
		for j in range(0,i+1):
			option[j]=np.exp(-r*dt)*(p*option[j]+(1-p)*option[j+1])#price of option as the discount of the expected future ones
			if typeEA=="American":
				ST[j]=np.exp(-r*dt)*(p*ST[j]+(1-p)*ST[j+1])
				option[j]=max(option[j], max(typeCP*(ST[j]-K),0)) # the vector option is the max of price of option and payoff if we exercise the option cuz american option can be alwayse exercised
				#the price in the vector is the max of these two and will be the one in the tree

	return option[0]