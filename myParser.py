
class Parser:

  col = 0

  ##### Parser header #####
  def __init__(self, scanner):
    self.next_token = scanner.next_token
    self.token = self.next_token()

  def take_token(self, token_type):
    if self.token.type != token_type:
      self.error("Unexpected token: %s" % token_type)
    if token_type != 'EOF':
      self.token = self.next_token()

  def error(self, msg):
    raise RuntimeError('Parser error, %s' % msg)

  ##### Parser body #####

  # Starting symbol
  def start(self):
    self.newline_stmt()
    # start -> newline program EOF
    if (self.token.type == 'version' or self.token.type == 'services' or self.token.type == 'volumes'
        or self.token.type == 'networks' or self.token.type == 'EOF'):
      self.program()
      self.take_token('EOF')
    else:
      self.error("Epsilon not allowed")

  def program(self):
    # program -> newline statement program
    self.newline_stmt()
    if (self.token.type == 'version' or self.token.type == 'services' or self.token.type == 'volumes'
        or self.token.type == 'networks'):
      self.statement()
      self.program()
    # program -> eps
    else:
      pass

  def statement(self):
    # statement -> version_stmt
    if self.token.type == 'version':
      self.version_stmt()
    # statement -> services_stmt
    elif self.token.type == 'services':
      self.services_stmt()
    # statement -> volumes_init_stmt
    elif self.token.type == 'volumes':
      self.volumes_init_stmt()
    # statement -> networks_init_stmt
    elif self.token.type == 'networks':
      self.networks_init_stmt()
    else:
      self.error("Epsilon not allowed")

  def version_stmt(self):
    # version_stmt -> VERSION single_value
    if self.token.type == 'version':
      self.take_token('version')
      self.single_value('VERSION_VAL')
      print("version_stmt OK")
    else:
      self.error("Epsilon not allowed")
   
  def services_stmt(self):
    # services_stmt -> SERVICES colon_stmt newline_stmt service_instances
    if self.token.type == 'services':
      self.take_token('services')
      self.colon_stmt()
      self.newline_stmt()
      self.service_instances(self.col)
      print("services_stmt OK")
    else:
      self.error("Epsilon not allowed")

  def service_instances(self, white_signs):
    # service_instances -> Eps
    # service_instances -> SCALAR colon_stmt newline_stmt service_config service_instances
    if (white_signs == self.col):
      if self.token.type == 'SCALAR':
        self.take_token('SCALAR')
      else:
        self.error("Scalar expected")
      self.colon_stmt()
      self.newline_stmt()
      self.service_config(self.col)
      print("service_instance OK")
      self.service_instances(white_signs)

  def service_config(self, white_signs):
    # service_config -> Eps
    if (white_signs == self.col):
      # service_config -> image_stmt service_config
      if self.token.type == 'image':
        self.image_stmt()
      # service_config -> ports_stmt service_config
      elif self.token.type == 'ports':
        self.ports_stmt()
      # service_config -> volumes_stmt service_config
      elif self.token.type == 'volumes':
        self.volumes_stmt()
      # service_config -> networks_stmt service_config
      elif self.token.type == 'networks':
        self.networks_stmt()
      # service_config -> deploy_stmt service_config
      elif self.token.type == 'deploy':
        self.deploy_stmt()
      # service_config -> build_stmt service_config
      elif self.token.type == 'build':
        self.build_stmt()
      # service_config -> environment_stmt service_config
      elif self.token.type == 'environment':
        self.environment_stmt()
      # service_config -> links_stmt service_config
      elif self.token.type == 'links':
        self.links_stmt()
      else:
        self.error("Epsilon not allowed")
      self.service_config(white_signs)

  def image_stmt(self):
    # image_stmt -> IMAGE single_value
    if self.token.type == 'image':
      self.take_token('image')
      self.single_value('SCALAR')
      print("image_stmt OK")
    else:
      self.error("Epsilon not allowed")

  def ports_stmt(self):
    # ports_stmt -> PORTS array
    if self.token.type == 'ports':
      self.take_token('ports')
      self.array('PORT_VAL')
      print("ports_stmt OK")
    else:
      self.error("Epsilon not allowed")

  def deploy_stmt(self):
    # deploy_stmt -> DEPLOY config_values
    if self.token.type == 'deploy':
      self.take_token('deploy')
      self.config_values()
      print("deploy_stmt OK")
    else:
      self.error("Epsilon not allowed")

  def environment_stmt(self):
    # environment_stmt -> ENVIRONMENT config_values
    if self.token.type == 'environment':
      self.take_token('environment')
      self.config_values()
      print("environment_stmt OK")
    else:
      self.error("Epsilon not allowed")

  def build_stmt(self):
    # build_stmt -> BUILD colon_stmt build_type
    if self.token.type == 'build':
      self.take_token('build')
      self.colon_stmt()
      self.build_type()
      print("build OK")
    else:
      self.error("Epsilon not allowed")

  def build_type(self):
    # build_type -> DOT newline_stmt
    if self.token.type == 'DOT':
      self.take_token('DOT')
      self.newline_stmt()
    # build_type -> newline_stmt config_value
    else:
      self.newline_stmt()
      self.config_value(self.col)

  def volumes_stmt(self):
    # volumes_stmt -> VOLUMES array
    if self.token.type == 'volumes':
      self.take_token('volumes')
      self.array('SCALAR')
      print("volumes_stmt OK")
    else:
      self.error("Epsilon not allowed")

  def networks_stmt(self):
    # networks_stmt -> NETWORKS array
    if self.token.type == 'networks':
      self.take_token('networks')
      self.array('SCALAR')
      print("networks_stmt OK")
    else:
      self.error("Epsilon not allowed")

  def links_stmt(self):
    # links_stmt -> LINKS array
    if self.token.type == 'links':
      self.take_token('links')
      self.array('SCALAR')
      print("links_stmt OK")
    else:
      self.error("Epsilon not allowed")

  def volumes_init_stmt(self):
    # volumes_init_stmt -> VOLUMES init_stmt
    if self.token.type == 'volumes':
      self.take_token('volumes')
      self.init_stmt()
      print("volumes_init_stmt OK")
    else:
      self.error("Epsilon not allowed")

  def networks_init_stmt(self):
    # networks_init_stmt -> NETWORKS init_stmt
    if self.token.type == 'networks':
      self.take_token('networks')
      self.init_stmt()
      print("networks_init_stmt OK")
    else:
      self.error("Epsilon not allowed")

  def init_stmt(self):
    # init_stmt -> colon_stmt newline_stmt init_value
    self.colon_stmt()
    self.newline_stmt()
    self.init_value(self.col)

  def init_value(self, white_signs):
    # init_value -> Eps
    # init_value -> SCALAR colon_stmt newline_stmt init_value
    if (white_signs == self.col):
      if self.token.type == 'SCALAR':
        self.take_token('SCALAR')
      else:
        self.error("SCALAR expected")
      self.colon_stmt()
      self.newline_stmt()
      self.init_value(white_signs)

  def colon_stmt(self):
    # colon_stmt -> skip_white_signs COLON skip_white_signs
    self.skip_white_signs()
    if self.token.type == 'COLON':
      self.take_token('COLON')
    else:
      self.error("Colon expected")
    self.skip_white_signs()

  def skip_white_signs(self):
    # skip_white_signs -> Eps
    if self.token.type != 'SPACE':
      return 0
    # skip_white_signs -> SPACE skip_white_signs
    else:
      self.take_token('SPACE')
      return 1 + self.skip_white_signs()

  def single_value(self, value_type):
    # single_value -> colon_stmt value_type skip_white_signs newline_stmt
    self.colon_stmt()
    # value_type -> SCALAR
    # value_type -> VERSION_VAL
    if self.token.type == value_type:
      self.take_token(value_type)
    else:
      self.error("Uexpected value type")
    self.skip_white_signs()
    self.newline_stmt()

  def array(self, array_type):
    # array -> colon_stmt newline_stmt array_value
    self.colon_stmt()
    self.newline_stmt()
    self.array_value(array_type, self.col)

  def array_value(self, array_type, white_signs):
    if white_signs == self.col:
      # array_value -> Eps
      # array_value -> DASH skip_white_signs array_type skip_white_signs newline_stmt array_value
      if self.token.type == 'DASH':
        self.take_token('DASH')
      else:
        self.error("DASH expected")
      self.skip_white_signs()
      # array_type -> SCALAR
      # array_type -> PORT_VAL
      if self.token.type == array_type:
        self.take_token(array_type)
      else:
        self.error("Unexpected array type")
      self.skip_white_signs()
      self.newline_stmt()
      self.array_value(array_type, white_signs)

  def config_values(self):
    # config_values -> colon_stmt skip_white_signs newline_stmt config_value
    self.colon_stmt()
    self.newline_stmt()
    self.config_value(self.col)

  def config_value(self, white_signs):
    if white_signs == self.col:
      # config_value -> Eps
      # config_value -> SCALAR single_value config_value
      if self.token.type == 'SCALAR':
        self.take_token('SCALAR')
      else:
        self.error("Scalar expected")
      self.single_value('SCALAR')
      self.config_value(white_signs)

  def newline_stmt(self):
    # newline_stmt -> Eps
    # newline_stmt -> NEWLINE skip_white_signs newline
    if self.token.type == 'NEWLINE':
      self.take_token('NEWLINE')
      self.col = self.skip_white_signs()
      self.newline_stmt()
    elif self.token.type == 'EOF':
      self.col = -1
