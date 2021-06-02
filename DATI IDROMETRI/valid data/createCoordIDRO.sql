USE [Hera]
GO

/****** Object:  Table [dbo].[coord_idro]    Script Date: 4/20/2021 8:28:26 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[coord_idro](
	[Nome] [nvarchar](70) NOT NULL,
	[lat] [float] NOT NULL,
	[long] [float] NOT NULL,
	[provincia] [nvarchar](50) NOT NULL,
 CONSTRAINT [PK_coord_idro] PRIMARY KEY CLUSTERED 
(
	[Nome] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


