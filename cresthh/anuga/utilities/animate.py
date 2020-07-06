"""
A module to allow interactive plotting in a Jupyter notebook of quantities and mesh
associated with an ANUGA domain and SWW file.
"""

import numpy as np
import os


class Domain_plotter:
    """
    A class to wrap ANUGA domain centroid values for stage, height, elevation
    xmomentunm and ymomentum, and triangulation information.
    """


    def __init__(self, domain, plot_dir='_plot', min_depth=0.01):

        self.plot_dir = plot_dir
        self.make_plot_dir()

        self.min_depth = min_depth
        
        self.nodes = domain.nodes
        self.triangles = domain.triangles
        self.x = domain.nodes[:, 0]
        self.y = domain.nodes[:, 1]

        self.xc = domain.centroid_coordinates[:, 0]
        self.yc = domain.centroid_coordinates[:, 1]

        self.xllcorner = domain.geo_reference.xllcorner
        self.yllcorner = domain.geo_reference.yllcorner
        self.zone = domain.geo_reference.zone

        import matplotlib.tri as tri
        self.triang = tri.Triangulation(self.x, self.y, self.triangles)

        self.elev = domain.quantities['elevation'].centroid_values
        self.stage = domain.quantities['stage'].centroid_values
        self.depth = self.stage - self.elev
        self.xmom = domain.quantities['xmomentum'].centroid_values
        self.ymom = domain.quantities['ymomentum'].centroid_values
        self.domain = domain

    def _depth_frame(self, figsize, dpi, vmin, vmax):

        import matplotlib.pyplot as plt

        name = self.domain.get_name()
        time = self.domain.get_time(relative_time=False).strftime('%Y%m%d%H%M%S')
        
        self.depth = self.stage - self.elev

        md = self.min_depth

        fig = plt.figure(figsize=figsize, dpi=dpi)

        plt.title('Depth: Time :%s'%(time))

        self.triang.set_mask(self.depth > md)
        plt.tripcolor(self.triang,
                      facecolors=self.elev,
                      cmap='Greys_r')


        self.triang.set_mask(self.depth <= md)
        plt.tripcolor(self.triang,
                      facecolors=self.depth,
                      cmap='viridis',
                      vmin=vmin, vmax=vmax)

        plt.colorbar()

    def save_depth_frame(self, figsize=(10, 6), dpi=80,
                         vmin=0.0, vmax=20):

        import matplotlib.pyplot as plt

        plot_dir = self.plot_dir
        name = self.domain.get_name()
        time = self.domain.get_time(relative_time=False).strftime('%Y%m%d%H%M%S')

        self._depth_frame(figsize, dpi, vmin, vmax)

        if plot_dir is None:
            plt.savefig(name+'_depth_%s.png'%(str(time)))
        else:
            plt.savefig(os.path.join(plot_dir, name
                                     + '_depth_%s.png'%(str(time))))
        plt.close()

    def plot_depth_frame(self, figsize=(5, 3), dpi=80,
                         vmin=0.0, vmax=20.0):

        import matplotlib.pyplot as plt

        self._depth_frame(figsize, dpi, vmin, vmax)

        plt.show()

    def make_depth_animation(self, save_gif=False, fps=None, dst=None):

        import numpy as np
        import glob
        from matplotlib import image, animation
        from matplotlib import pyplot as plt

        plot_dir = self.plot_dir
        name = self.domain.get_name()
        time = self.domain.get_time(relative_time=False).strftime('%Y%m%d%H%M%S')

        if plot_dir is None:
            expression = name+'_depth_*.png'
        else:
            expression = os.path.join(plot_dir, name+'_depth_*.png')
        img_files = sorted(glob.glob(expression))

        figsize = (10, 6)

        fig = plt.figure(figsize=figsize, dpi=80)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')  # so there's not a second set of axes
        im = plt.imshow(image.imread(img_files[0]))

        def init():

            im.set_data(image.imread(img_files[0]))
            return im,

        def animate(i):

            image_i = image.imread(img_files[i])
            im.set_data(image_i)
            return im,

        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                       frames=len(img_files), interval=200, blit=True)
        #include opportunity to save as gif
        if save_gif:
            mywriter = animation.FFMpegWriter(fps=1)
            anim.save(dst)

        plt.close()

        return anim

    def _stage_frame(self, figsize, dpi, vmin, vmax):

        import matplotlib.pyplot as plt

        name = self.domain.get_name()
        time = self.domain.get_time(relative_time=False).strftime('%Y%m%d%H%M%S')
        
        self.depth = self.stage - self.elev

        md = self.min_depth

        fig = plt.figure(figsize=figsize, dpi=dpi)

        plt.title('Stage: Time %s'%s(time))

        self.triang.set_mask(self.depth > md)
        plt.tripcolor(self.triang,
                      facecolors=self.elev,
                      cmap='Greys_r')

        self.triang.set_mask(self.depth <= md)
        plt.tripcolor(self.triang,
                      facecolors=self.stage,
                      cmap='viridis',
                      vmin=vmin, vmax=vmax)

        plt.colorbar()

    def save_stage_frame(self, figsize=(10, 6), dpi=80,
                         vmin=-20.0, vmax=20.0):

        import matplotlib.pyplot as plt

        plot_dir = self.plot_dir
        name = self.domain.get_name()
        time = self.domain.get_time(relative_time=False).strftime('%Y%m%d%H%M%S')

        self._stage_frame(figsize, dpi, vmin, vmax)

        if plot_dir is None:
            plt.savefig(name+'_stage_%s.png'%s(str(time)))
        else:
            plt.savefig(os.path.join(plot_dir, name
                                     + '_stage_%s.png'.format(str(time))))
        plt.close()

    def plot_stage_frame(self, figsize=(5, 3), dpi=80,
                         vmin=-20.0, vmax=20.0):

        import matplotlib.pyplot as plt

        self._stage_frame(figsize, dpi, vmin, vmax)

        plt.show()

    def make_stage_animation(self, save_gif=False, fps=None, dst=None):

        import numpy as np
        import glob
        from matplotlib import image, animation
        from matplotlib import pyplot as plt

        plot_dir = self.plot_dir
        name = self.domain.get_name()
        time = self.domain.get_time(relative_time=False).strftime('%Y%m%d%H%M%S')

        if plot_dir is None:
            expression = name+'_stage_*.png'
        else:
            expression = os.path.join(plot_dir, name+'_stage_*.png')

        img_files = sorted(glob.glob(expression))

        figsize = (10, 6)

        fig = plt.figure(figsize=figsize, dpi=80)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')  # so there's not a second set of axes
        im = plt.imshow(image.imread(img_files[0]))

        def init():

            im.set_data(image.imread(img_files[0]))
            return im,

        def animate(i):

            image_i = image.imread(img_files[i])
            im.set_data(image_i)
            return im,

        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                       frames=len(img_files), interval=200, blit=True)
        if save_gif:
            mywriter = animation.FFMpegWriter(fps=1)
            anim.save(dst)
        plt.close()

        return anim

    def _speed_frame(self, figsize, dpi, vmin, vmax):

        import matplotlib.pyplot as plt

        name = self.domain.get_name()
        time = self.domain.get_time(relative_time=False).strftime('%Y%m%d%H%M%S')
        
        self.depth = self.stage - self.elev

        md = self.min_depth

        fig = plt.figure(figsize=figsize, dpi=dpi)

        plt.title('Speed: Time %s'%(time))

        self.triang.set_mask(self.depth > md)
        plt.tripcolor(self.triang,
                      facecolors=self.elev,
                      cmap='Greys_r')

        self.triang.set_mask(self.depth <= md)
        plt.tripcolor(self.triang,
                      facecolors=self.speed,
                      cmap='viridis',
                      vmin=vmin, vmax=vmax)

        plt.colorbar()

    def save_speed_frame(self, figsize=(10, 6), dpi=80,
                         vmin=-20.0, vmax=20.0):

        import matplotlib.pyplot as plt

        plot_dir = self.plot_dir
        name = self.domain.get_name()
        time = self.domain.get_time(relative_time=False).strftime('%Y%m%d%H%M%S')

        self._speed_frame(figsize, dpi, vmin, vmax)

        if plot_dir is None:
            plt.savefig(name+'_speed_%s.png'%s(str(time)))
        else:
            plt.savefig(os.path.join(plot_dir, name
                                     + '_speed_%s.png'%s(str(time))))
        plt.close()

    def plot_speed_frame(self, figsize=(5, 3), dpi=80,
                         vmin=-20.0, vmax=20.0):

        import matplotlib.pyplot as plt

        self._speed_frame(figsize, dpi, vmin, vmax)

        plt.show()

    def make_speed_animation(self, save_gif=False, fps=None, dst=None):

        import numpy as np
        import glob
        from matplotlib import image, animation
        from matplotlib import pyplot as plt

        plot_dir = self.plot_dir
        name = self.domain.get_name()
        time = self.domain.get_time(relative_time=False).strftime('%Y%m%d%H%M%S')

        if plot_dir is None:
            expression = name+'_speed_*.png'
        else:
            expression = os.path.join(plot_dir, name+'_speed_*.png')

        img_files = sorted(glob.glob(expression))

        figsize = (10, 6)

        fig = plt.figure(figsize=figsize, dpi=80)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')  # so there's not a second set of axes
        im = plt.imshow(image.imread(img_files[0]))

        def init():

            im.set_data(image.imread(img_files[0]))
            return im,

        def animate(i):

            image_i = image.imread(img_files[i])
            im.set_data(image_i)
            return im,

        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                       frames=len(img_files), interval=200, blit=True)
        if save_gif:
            mywriter = animation.FFMpegWriter(fps=1)
            anim.save(dst)
            
        plt.close()

        return anim
    
    #TODO make cross section frame
    def plot_cross_section_frame(self, figsize=(5, 3)):
        pass

    #TODO make cross section animations
    def make_cross_section_profile_animation(self):
        pass

    def make_plot_dir(self, clobber=True):
        """
        Utility function to create a directory for storing a sequence of plot
        files, or if the directory already exists, clear out any old plots.
        If clobber==False then it will abort instead of deleting existing files.
        """

        plot_dir = self.plot_dir
        if plot_dir is None:
            return
        else:
            import os
            if os.path.isdir(plot_dir):
                if clobber:
                    os.system("rm %s/*" % plot_dir)
                else:
                    raise IOError(
                        '*** Cannot clobber existing directory %s' % plot_dir)
            else:
                os.system("mkdir %s" % plot_dir)
            print "Figure files for each frame will be stored in " + plot_dir

    


class SWW_plotter:
    """
    A class to wrap ANUGA swwfile centroid values for stage, height, elevation
    xmomentunm and ymomentum, and triangulation information.
    """

    def __init__(self, swwfile='domain.sww', plot_dir='_plot',
                 min_depth = 0.01,
                 minimum_allowed_depth=1.0e-03,
                 start_time=None,
                 make_dir=True):

        self.plot_dir = plot_dir
        if make_dir:
            self.make_plot_dir()
        
        self.min_depth = min_depth

        import matplotlib.tri as tri
        import numpy as np

        import os
        self.name = os.path.splitext(swwfile)[0]

        from cresthh.anuga.file.netcdf import NetCDFFile
        p = NetCDFFile(swwfile)

        self.x = np.array(p.variables['x'])
        self.y = np.array(p.variables['y'])
        self.triangles = np.array(p.variables['volumes'])

        vols0 = self.triangles[:, 0]
        vols1 = self.triangles[:, 1]
        vols2 = self.triangles[:, 2]

        self.triang = tri.Triangulation(self.x, self.y, self.triangles)

        self.xc = (self.x[vols0]+self.x[vols1]+self.x[vols2])/3.0
        self.yc = (self.y[vols0]+self.y[vols1]+self.y[vols2])/3.0

        self.xllcorner = p.xllcorner
        self.yllcorner = p.yllcorner
        self.zone = p.zone

        self.elev = np.array(p.variables['elevation_c'])
        self.stage = np.array(p.variables['stage_c'])
        self.xmom = np.array(p.variables['xmomentum_c'])
        self.ymom = np.array(p.variables['ymomentum_c'])
        self.exc_rain= np.array(p.variables['excess_rain_c'])
        self.SM= np.array(p.variables['SM_c'])*100 # To %
        # self.SI0= np.array(p.variables['SI0_c'])
        # self.SS0= np.array(p.variables['SS0_c'])

        self.depth = np.zeros_like(self.stage)
        if(len(self.elev.shape) == 2):
            self.depth = self.stage - self.elev
        else:
            for i in range(self.depth.shape[0]):
                self.depth[i, :] = self.stage[i, :]-self.elev

        self.xvel = np.where(self.depth > minimum_allowed_depth,
                             self.xmom / self.depth, 0.0)
        self.yvel = np.where(self.depth > minimum_allowed_depth,
                             self.ymom / self.depth, 0.0)

        self.speed = np.sqrt(self.xvel**2 + self.yvel**2)

        if start_time:
            import pandas
            import datetime
            if isinstance(start_time, pandas._libs.tslibs.timestamps.Timestamp):
                self.time= [(start_time + datetime.timedelta(seconds=second)) for second in np.array(p.variables['time'])]
            else:
                msg= 'expected pandas timestamp, pd.to_datetime()'
                raise Exception(msg)
            self._abs_time=True
        else:
            self.time = np.array(p.variables['time'])
            self._abs_time=False

    def _depth_frame(self, figsize, dpi, frame, vmin, vmax, cmap='viridis'):

        import matplotlib.pyplot as plt

        name = self.name
        if self._abs_time:
            time = self.time[frame].strftime('%Y%m%d %H:%M:%S')
        else:
            time= self.time[frame]
        depth = self.depth[frame, :]
        
        md = self.min_depth
        
        try:
            elev = self.elev[frame, :]
        except:
            elev = self.elev

        ims = []

        fig = plt.figure(figsize=figsize, dpi=dpi)

        plt.title('Depth: Time %s'%(time))

        self.triang.set_mask(depth > md)
        plt.tripcolor(self.triang,
                      facecolors=elev,
                      cmap='Greys_r')

        self.triang.set_mask(depth < md)
        plt.tripcolor(self.triang,
                      facecolors=depth,
                      cmap=cmap,
                      vmin=vmin, vmax=vmax)

        cbar= plt.colorbar()
        cbar.set_label('m', fontsize=15)

    def save_depth_frame(self, figsize=(10, 6), dpi=160, frame=-1,
                         vmin=0.0, vmax=20.0, cmap='viridis'):

        import matplotlib.pyplot as plt

        name = self.name
        if self._abs_time:
            time = self.time[frame].strftime('%Y%m%d %H:%M:%S')
        else:
            time= self.time[frame]
        plot_dir = self.plot_dir

        self._depth_frame(figsize, dpi, frame, vmin, vmax,cmap)

        if plot_dir is None:
            plt.savefig(name+'_depth_%s.png'%(str(time)))
        else:
            plt.savefig(os.path.join(plot_dir, name
                                     + '_depth_%s.png'%(str(time))))
        plt.close()

    def plot_depth_frame(self, figsize=(5, 3), dpi = 80, frame=-1,
                         vmin=0.0, vmax=20.0):

        import matplotlib.pyplot as plt

        self._depth_frame(figsize, dpi, frame, vmin, vmax)

        plt.show()

    def _stage_frame(self, figsize, dpi, frame, vmin, vmax):

        import matplotlib.pyplot as plt

        name = self.name
        if self._abs_time:
            time = self.time[frame].strftime('%Y%m%d %H:%M:%S')
        else:
            time= self.time[frame]
        stage = self.stage[frame, :]
        depth = self.depth[frame, :]
        
        md = self.min_depth
        
        try:
            elev = self.elev[frame, :]
        except:
            elev = self.elev

        ims = []

        fig = plt.figure(figsize=figsize, dpi=dpi)

        plt.title('Stage: Time %s'%(time))

        self.triang.set_mask(depth > md)
        plt.tripcolor(self.triang,
                      facecolors=elev,
                      cmap='Greys_r')

        self.triang.set_mask(depth < md)
        plt.tripcolor(self.triang,
                      facecolors=stage,
                      cmap='viridis',
                      vmin=vmin, vmax=vmax)

        cbar= plt.colorbar()
        cbar.set_label('m', fontsize=15)

    def save_stage_frame(self, figsize=(10, 6), dpi=160, frame=-1,
                         vmin=-20.0, vmax=20.0):

        import matplotlib.pyplot as plt

        name = self.name
        if self._abs_time:
            time = self.time[frame].strftime('%Y%m%d %H:%M:%S')
        else:
            time= self.time[frame]
        plot_dir = self.plot_dir

        self._stage_frame(figsize, dpi, frame, vmin, vmax)

        if plot_dir is None:
            plt.savefig(name+'_stage_%s.png'%s(str(time)))
        else:
            plt.savefig(os.path.join(plot_dir, name
                                     + '_stage_%s.png'%(str(time))))
        plt.close()

    def plot_stage_frame(self, figsize=(5, 3), dpi=80, frame=-1,
                         vmin=-20, vmax=20.0):

        import matplotlib.pyplot as plt

        self._stage_frame(figsize, dpi, frame, vmin, vmax)

        plt.show()

    def _speed_frame(self, figsize, dpi, frame, vmin, vmax):

        import matplotlib.pyplot as plt

        name = self.name
        if self._abs_time:
            time = self.time[frame].strftime('%Y%m%d %H:%M:%S')
        else:
            time= self.time[frame]
        depth = self.depth[frame, :]
        
        md = self.min_depth
        
        try:
            elev = self.elev[frame, :]
        except:
            elev = self.elev
        speed = self.speed[frame, :]

        ims = []

        fig = plt.figure(figsize=figsize, dpi=dpi)

        plt.title('Speed: Time %s'%(time))

        self.triang.set_mask(depth > md)
        plt.tripcolor(self.triang,
                      facecolors=elev,
                      cmap='Greys_r')

        self.triang.set_mask(depth < md)
        plt.tripcolor(self.triang,
                      facecolors=speed,
                      cmap='viridis',
                      vmin=vmin, vmax=vmax)

        cbar= plt.colorbar()
        cbar.set_label('m/s', fontsize=15)

    def save_speed_frame(self, figsize=(10, 6), dpi=160, frame=-1,
                         vmin=0.0, vmax=10.0):

        import matplotlib.pyplot as plt

        name = self.name
        if self._abs_time:
            time = self.time[frame].strftime('%Y%m%d %H:%M:%S')
        else:
            time= self.time[frame]
        plot_dir = self.plot_dir

        self._speed_frame(figsize, dpi, frame, vmin, vmax)

        if plot_dir is None:
            plt.savefig(name+'_speed_%s.png'.format(str(time)))
        else:
            plt.savefig(os.path.join(plot_dir, name
                                     + '_speed_%s.png'%(str(time))))
        plt.close()

    def plot_speed_frame(self, figsize=(5, 3), dpi=80, frame=-1,
                         vmin=0.0, vmax=10.0):

        import matplotlib.pyplot as plt

        self._speed_frame(figsize, dpi, frame, vmin, vmax)

        plt.show()

    def _soil_frame(self, figsize, dpi, frame, vmin, vmax):
    
        import matplotlib.pyplot as plt

        name = self.name
        if self._abs_time:
            time = self.time[frame].strftime('%Y%m%d %H:%M:%S')
        else:
            time= self.time[frame]
        soil = self.SM[frame, :]
        depth= self.depth[frame, :]
        md = self.min_depth
        
        try:
            elev = self.elev[frame, :]
        except:
            elev = self.elev

        fig = plt.figure(figsize=figsize, dpi=dpi)

        plt.title('Soil moisture: Time %s'%(time))

        self.triang.set_mask(depth > md)
        plt.tripcolor(self.triang,
                      facecolors=elev,
                      cmap='Greys_r')

        self.triang.set_mask(depth < md)
        plt.tripcolor(self.triang,
                      facecolors=soil,
                      cmap='viridis',
                      vmin=vmin, vmax=vmax)

        cbar= plt.colorbar()
        cbar.set_label('%', fontsize=15)

    def save_soil_frame(self, figsize=(10, 6), dpi=160, frame=-1,
                         vmin=0.0, vmax=100.0):

        import matplotlib.pyplot as plt

        name = self.name
        if self._abs_time:
            time = self.time[frame].strftime('%Y%m%d %H:%M:%S')
        else:
            time= self.time[frame]
        plot_dir = self.plot_dir

        self._soil_frame(figsize, dpi, frame, vmin, vmax)

        if plot_dir is None:
            plt.savefig(name+'_soil_%s.png'.format(str(time)))
        else:
            plt.savefig(os.path.join(plot_dir, name
                                     + '_soil_%s.png'%(str(time))))
        plt.close()

    def plot_soil_frame(self, figsize=(5, 3), dpi=80, frame=-1,
                         vmin=0.0, vmax=50.0):

        import matplotlib.pyplot as plt

        self._soil_frame(figsize, dpi, frame, vmin, vmax)

        plt.show()        

    #MODIFIED BY ALLEN LI 2020/06/17
    def _longitudinal_frame(self, figsize, dpi, frame, pnts):
        '''
        Plot cross-section profile/longitutional profile with given pnts

        Inputs:
        -----------------------
        pnts - List; a sequence of points with their coordinates
        '''
        import matplotlib.pyplot as plt

        name = self.name
        if self._abs_time:
            time = self.time[frame].strftime('%Y%m%d %H:%M:%S')
        else:
            time= self.time[frame]
        depths = []
        stages= []
        ilocs= []
        dists= []
        #order by distance starting from origin
        for pnt in pnts:
            dist= (pnt[0]-self.xllcorner)**2+(pnt[1]-self.yllcorner)**2
            iloc= np.argmin((pnt[0]-self.xc-self.xllcorner)**2+(pnt[1]-self.yc-self.yllcorner)**2)
            stage= self.stage[frame,iloc]
            depth= self.depth[frame,iloc]
            dists.append(dist)
            ilocs.append(iloc)
            stages.append(stage)
            depths.append(depth)
        ilocs= np.array(ilocs)
        stages= np.array(stages)
        depths= np.array(depths)
        dists= np.array(dists)
        ranks= np.argsort(dists)
        stages= stages[ranks]
        depths= depths[ranks]
        dists= dists[ranks]
        fig = plt.figure(figsize=figsize, dpi=dpi)
        plt.title('Channel profile: Time %s'%(time))
        plt.plot(dists, stages,color='b')
        plt.plot(dists, stages-depths, color='k')
        plt.fill_between(dists, stages-depths, stages, color='aqua')

    def save_longitudinal_frame(self, pnts, figsize=(15, 6), dpi=160, frame=-1):
        name = self.name
        if self._abs_time:
            time = self.time[frame].strftime('%Y%m%d %H:%M:%S')
        else:
            time= self.time[frame]
        plot_dir = self.plot_dir
        import matplotlib.pyplot as plt
        self._longitudinal_frame(figsize, dpi, frame, pnts)

        if plot_dir is None:
            plt.savefig(name+'_channel_%s.png'.format(str(time)))
        else:
            plt.savefig(os.path.join(plot_dir, name
                                     + '_channel_%s.png'%(str(time))))
        plt.close()        
    
    def plot_longitudinal_frame(self,pnts, figsize=(15, 6), dpi=80, frame=-1):

        import matplotlib.pyplot as plt

        self._longitudinal_frame(figsize, dpi, frame, pnts)

        plt.show()


    def make_depth_animation(self, save_gif=False, dst='temp.gif'):

        return self._make_quantity_animation(quantity='depth', save_gif=False, dst='temp.gif')

    def make_speed_animation(self, save_gif=False, dst='temp.gif'):

        return self._make_quantity_animation(quantity='speed', save_gif=False, dst='temp.gif')

    def make_stage_animation(self, save_gif=False, dst='temp.gif'):

        return self._make_quantity_animation(quantity='stage', save_gif=False, dst='temp.gif')

    def make_longitudinal_animation(self, save_gif=False, dst='temp.gif'):

        return self._make_quantity_animation(quantity='channel', save_gif=False, dst='temp.gif')

    def make_soil_animation(self, save_gif=False, dst='temp.gif'):
    
        return self._make_quantity_animation(quantity='soil', save_gif=False, dst='temp.gif')        

    def _make_quantity_animation(self, quantity='depth', save_gif=False, dst='temp.gif'):

        import numpy as np
        import glob
        from matplotlib import image, animation
        from matplotlib import pyplot as plt

        plot_dir = self.plot_dir
        name = self.name

        if plot_dir is None:
            expression = name+'_'+quantity+'_*.png'
        else:
            expression = os.path.join(plot_dir, name+'_'+quantity+'_*.png')
        img_files = sorted(glob.glob(expression))

        figsize = (10, 6)
        if quantity=='channel':
            figsize=(15,6)

        fig = plt.figure(figsize=figsize, dpi=80)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')  # so there's not a second set of axes
        im = plt.imshow(image.imread(img_files[0]))

        def init():
            im.set_data(image.imread(img_files[0]))
            return im,

        def animate(i):
            image_i = image.imread(img_files[i])
            im.set_data(image_i)
            return im,

        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                       frames=len(img_files),
                                       interval=200, blit=True)
        if save_gif:
            mywriter = animation.FFMpegWriter(fps=10)
            anim.save(dst)
        plt.close()

        return anim

    def make_plot_dir(self, clobber=True):
        """
        Utility function to create a directory for storing a sequence of plot
        files, or if the directory already exists, clear out any old plots.
        If clobber==False then it will abort instead of deleting existing files.
        """

        plot_dir = self.plot_dir
        if plot_dir is None:
            return
        else:
            import os
            if os.path.isdir(plot_dir):
                if clobber:
                    os.system("rm %s/*" % plot_dir)
                else:
                    raise IOError(
                      '*** Cannot clobber existing directory %s' % plot_dir)
            else:
                os.system("mkdir %s" % plot_dir)
            print "Figure files for each frame will be stored in " + plot_dir
