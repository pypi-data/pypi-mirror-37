from enum import Enum


class Channel:
    sampler = None
    target_node = None
    target_path = None

    def __init__(self, channel=None, gltf=None, animation=None,
                 sampler=None, target_node=None, target_path=None):
        if channel:
            if 'sampler' in channel:
                self.sampler = animation.samplers[channel['sampler']]
            target = channel.get('target')
            if target:
                if 'node' in target:
                    self.target_node = gltf.nodes[target['node']]
                if 'path' in target:
                    self.target_path = target['path']
        else:
            self.sampler = sampler
            self.target_node = target_node
            self.target_path = target_path

    def render(self, gltf=None, animation=None):
        channel = {
            'target': {
                'path': self.target_path
            }
        }

        if self.target_node:
            channel['target']['node'] = gltf.index_node(self.target_node)

        if self.sampler:
            if self.sampler not in animation.samplers:
                animation.samplers.append(self.sampler)
            channel['sampler'] = animation.samplers.index(self.sampler)

        return channel


class Sampler:
    class Interpolation(Enum):
        LINEAR = 'LINEAR'
        STEP = 'STEP'
        CUBICSPLINE = 'CUBICSPLINE'

    input = None
    output = None
    interpolation = Interpolation.LINEAR

    def __init__(self, sampler=None, gltf=None, input=None, output=None, interpolation=None):
        if sampler:
            if 'interpolation' in sampler:
                self.interpolation = self.Interpolation(sampler['interpolation'])
            if 'input' in sampler:
                self.input = gltf.accessors[sampler['input']]
            if 'output' in sampler:
                self.output = gltf.accessors[sampler['output']]
        else:
            self.interpolation = interpolation
            self.input = input
            self.output = output

    def render(self, gltf):
        sampler = {
            'input': gltf.index('accessors', self.input),
            'output': gltf.index('accessors', self.output),
        }

        if self.interpolation is not self.Interpolation.LINEAR:
            sampler['interpolation'] = self.interpolation.value

        return sampler


class Animation:
    channels = None
    samplers = None
    name = None

    def __init__(self, animation=None, gltf=None, channels=None, samplers=None, name=None):
        if animation:
            self.samplers = [Sampler(s, gltf) for s in animation.get('samplers', [])]
            self.channels = [Channel(c, gltf, self) for c in animation.get('channels', [])]
            self.name = animation.get('name')
        else:
            self.samplers = samplers if samplers is not None else []
            self.channels = channels if channels is not None else []
            self.name = name

    def render(self, gltf):
        animation = {
            'channels': [c.render(gltf, self) for c in self.channels],
            'samplers': [s.render(gltf) for s in self.samplers],
        }

        if self.name:
            animation['name'] = self.name

        return animation


class Skin:
    inverse_bind_matrices = None
    skeleton = None
    joints = None
    name = None

    def __init__(self, skin=None, gltf=None, inverse_bind_matrices=None,
                 skeleton=None, joints=None, name=None):
        if skin:
            self.joints = [gltf.nodes[idx] for idx in skin.get('joints', [])]
            if 'inverseBindMatrices' in skin:
                self.inverse_bind_matrices = gltf.accessors[skin['inverseBindMatrices']]
            if 'skeleton' in skin:
                self.skeleton = gltf.nodes[skin['skeleton']]
            self.name = skin.get('name')
        else:
            self.joints = joints if joints is not None else []
            self.inverse_bind_matrices = inverse_bind_matrices
            self.skeleton = skeleton
            self.name = name

    def render(self, gltf):
        skin = {
            'joints': [gltf.index_node(j) for j in self.joints]
        }

        if self.inverse_bind_matrices:
            skin['inverseBindMatrices'] = gltf.index('accessors', self.inverse_bind_matrices)
        if self.skeleton:
            skin['skeleton'] = gltf.index_node(self.skeleton)
        if self.name:
            skin['name'] = self.name

        return skin
