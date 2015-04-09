"""
This module represents a cluster's computational node.

Computer Systems Architecture Course
Assignment 1 - Cluster Activity Simulation
March 2015
"""
from threading import Thread, Lock, Event, Condition 
from cond_barrier import ReusableBarrierCond
from worker import Worker 
from task import Task
class Node:
    """
    Class that represents a cluster node with computation and storage
    functionalities.
    """

    def __init__(self, node_id, data):
        """
        Constructor.

        @type node_id: Integer
        @param node_id: the unique id of this node; between 0 and N-1

        @type data: List of Integer
        @param data: a list containing this node's data
        """
        self.node_id = node_id
        self.data = data
        # temporary buffer for needed for scatter 
	self.copy = data[:]
        self.lock_copy = Lock()
        self.nodes = None
        self.lock_data = Lock()
        # list of threads (in this case 16 fo each node)
	self.thread_list = []
	# list with tasks that need to be computed
        self.thread_pool = []
        self.mutex = Lock()
        # condition used for put and get
	self.condition = Condition(self.mutex)
	# condition needed for checking if there are 
	# still tasks that need o be solved
        self.all_tasks_done = Condition(self.mutex)
	# number of unfinished tasks
        self.unfinished_tasks = 0
        # start the 16 threads
	for i in range(16):
            th = Worker(self, i)
            self.thread_list.append(th)
            th.start()
    def __str__(self):
        """
        Pretty prints this node.

        @rtype: String
        @return: a string containing this node's id
        """
        return "Node %d" % self.node_id
    
    
    def set_cluster_info(self,  nodes):
        """
        Informs the current node about the supervisor and about the other
        nodes in the cluster.
        Guaranteed to be called before the first call to 'schedule_task'.

        @type nodes: List of Node
        @param nodes: a list containing all the nodes in the cluster
        """
        self.nodes = nodes
        # only one barrier shared by all the nodes in the cluster
        if self.node_id == 0:
            self.barrier = ReusableBarrierCond(len(self.nodes))
            self.barrier1 = ReusableBarrierCond(len(self.nodes))
        else:
            self.barrier = self.nodes[0].barrier
            self.barrier1 = self.nodes[0].barrier1
    
    def schedule_task(self, task, in_slices, out_slices):
        """
        Schedule task to execute on the node.

        @type task: Task
        @param task: the task object to execute

        @type in_slices: List of (Integer, Integer, Integer)
        @param in_slices: a list of the slices of data that need to be
            gathered for the task; each tuple specifies the id of a node
            together with the starting and ending indexes of the slice; the
            ending index is exclusive

        @type out_slices: List of (Integer, Integer, Integer)
        @param out_slices: a list of slices where the data produced by the
            task needs to be scattered; each tuple specifies the id of a node
            together with the starting and ending indexes of the slice; the
            ending index is exclusive
        """
        # adds a new task to be processed
	self.condition.acquire()
        self.thread_pool.append((task, in_slices, out_slices))
        self.unfinished_tasks += 1 
        self.condition.notify()
	self.condition.release()
    def sync_results(self):
        """
        Wait for scheduled tasks to finish and write results.
        """
        # waits until there is no unfinished task
	self.all_tasks_done.acquire()
	while self.unfinished_tasks:
		self.all_tasks_done.wait()
	self.all_tasks_done.release()
        self.barrier.wait()
	# updates data based on teh values from the scatter stage
        self.data = self.copy[:]
        self.barrier.wait()
  
    def get_data(self):
        """
        Return a copy of this node's data.
        """
        self.lock_data.acquire()
        aux = self.data[:]
        self.lock_data.release()
        
        return aux


    def shutdown(self):
        """
        Instructs the node to shutdown (terminate all threads). This method
        is invoked by the tester. This method must block until all the threads
        started by this node terminate.
        """
	# sending a "fake" task to do in order to 
	# notify shutdown
        for i in self.thread_list:
            self.condition.acquire()
            self.thread_pool.append((None, [], []))
            self.condition.notify()
            self.condition.release()
	
	# waits all threads to finish
        for th in self.thread_list:
            th.join()
