import matplotlib.pyplot as plt
import seaborn as sns


class PlotFormatter():
	'''Generic PlotFormatter class for creating in the ggplot style.
		
	Attributes:
		fig_width (int): width of figure that holds subplots
		fig_height (int): height of figure that holds subplots
		title (str): title of graph
		x_label (str): x-label title
		y_label (str): y-label title
	'''

	def __init__(self, fig_width, fig_height, title, x_label, y_label):

		self.fig_width = fig_width
		self.fig_height = fig_height
		self.title = title
		self.x_label = x_label
		self.y_label = y_label


		with plt.style.context(('ggplot')):
			self.fig, self.ax = plt.subplots(1,1, figsize=(self.fig_width, \
											self.fig_height))

			self.ax.set_title(self.title)
			self.ax.set_xlabel(self.x_label)
			self.ax.set_ylabel(self.y_label)
	

class ScatterPlot(PlotFormatter):
	'''Formatting ggplot-stype scatter plot
	
	Attributes:
		fig_width (int): width of figure that holds subplots
		fig_height (int): height of figure that holds subplots
		x (array): array to be shown in the x-axis
		y (array): array to be shown in the y-axis
		title (str): title of graph
		x_label (str): x-label title
		y_label (str): y-label title

	Optional:
		hue (categorical array): separates points on plot based off array
		alpha (float): adds transparncy to data points 
	'''
	def __init__(self, fig_width, fig_height, x, y, title, \
				x_label, y_label, hue=None, alpha=None, palette="muted"):
		PlotFormatter.__init__(self, fig_width, fig_height, title, x_label, y_label)

		self.x = x
		self.y = y

		if hue is None:
			self.hue = None
		else:
			self.hue = hue

		if alpha is None:
			self.alpha = None
		else:
			self.alpha = alpha

		self.palette = palette


		sns.scatterplot(self.x, self.y, hue=self.hue, alpha=self.alpha, \
						palette=self.palette)
