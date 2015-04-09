from threading import Thread
class Worker(Thread):
    
    def __init__(self, node, w_id):
        Thread.__init__(self)
        self.w_id = w_id
        self.node = node
        self.res = []
    def run(self):
            while(True):
		# blocks until there is task to process
		self.node.condition.acquire()
		while not self.node.thread_pool:
			self.node.condition.wait()
		req = self.node.thread_pool.pop(0)
		self.node.condition.release()
                # if  shutdown task
		if req[0] is None:
                    break
                task = req[0]
                self.res = []
		# gather stage
                for (n,start,end) in req[1]:
                    self.node.nodes[n].lock_data.acquire()
                    var = self.node.nodes[n].data[start:end]
                    self.node.nodes[n].lock_data.release()
                    self.res.extend(var)
                
		self.res = task.run(self.res)
                # scatter stage 
		cont = 0
                for (n, start, end) in req[2]:
                    source = self.res[cont: cont + (end-start)]
                    self.node.nodes[n].lock_copy.acquire()
                    z = [x + y for x, y in zip(source,self.node.nodes[n].copy[start:end])]
                    self.node.nodes[n].copy[start:end] = z[:]
                    self.node.nodes[n].lock_copy.release()
                    cont += (end - start)
		# task is computed => unfinished_tasks --
                self.node.all_tasks_done.acquire()
		unfinished = self.node.unfinished_tasks -1
		if unfinished == 0:
			self.node.all_tasks_done.notify_all()
		self.node.unfinished_tasks = unfinished
		self.node.all_tasks_done.release()
